import socket
import select
import requests
import json
import base64
import os
from time import sleep
from urllib.parse import urlparse, urlunparse
from http.server import BaseHTTPRequestHandler
from config.setsqlite import get_connection, isurlindb, insert_list_type, inserturl
import config.main_config as main_config
import config.resources as resources
from server.local_file_adapter import LocalFileAdapter
import server.vt_response_parser as vt_response_parser
import logger.logger as logger
from server.icon import systrayIcon


from requests_testadapter import TestAdapter, TestSession

__config__file__ = 'config.rdef'
__working__directory__ = os.getcwd()
resources_instance = resources.resources()


class ProxyRequestHandler(BaseHTTPRequestHandler):
    logger_instance = logger.logger()
    logger_instance.create_logger()
    config_instance = main_config.MainConfig()
    api_url, api_key = config_instance.read_configuration(
        __working__directory__, __config__file__)
    vt_response_parser_instance = vt_response_parser.vt_response_parser()
    protocol_version = 'HTTP/1.1'
    # Var
    conn = get_connection()  # Setting the SQL
    icon = systrayIcon()
    icon.start_icon_thread()

    def do_HEAD(self):
        self.do_GET(body=False)

    def _connect_to(self, netloc, soc):
        i = netloc.find(':')
        if i >= 0:
            host_port = netloc[:i], int(netloc[i+1:])
        else:
            host_port = netloc, 80
        try:
            soc.connect(host_port)
        except socket.error as e:
            try:
                msg = e
            except:
                msg = e
            self.send_error(404, msg)
            return 0
        return 1

    def do_GET(self):
        '''Function handles Http requests and calls checkUrl in order to detect risk
           In case the checkurl returns there is no risk (True), and record doesnt exist
           in the db, will insert to the whitelist database table, if (False) Will load Error page
           Blocked URL and will insert to DB'''
        (scm, netloc, path, params, query, fragment) = urlparse(self.path, 'http')
        if scm != 'http' or fragment or not netloc:  # Link Validity
            self.send_error(400, "bad url %s" % self.path)
            return
        url = scm + '://' + netloc
        # If function returns CHECK, we will check the link
        link_Status = isurlindb(self.conn, url)
        if(link_Status == 'CHECK'):
            if(self.checkUrl(url)):
                print("\n[*] Harmless url forwarding")
                self.socket_connection(netloc, path, params, query)
                inserturl(self.conn, 0, self.path, 0, 0,
                          0, scm)  # Insert to DB whitelist
                insert_list_type(self.conn, url, 0, 'rdef_web_whitelist', scm)
            else:  # Malicious, inserting to DB
                print("\n[!] Malicious url blocked")
                # Insert checked and malicious link to blacklist

                if self.load_blocked_page(url, alert=True):
                    self.socket_connection(netloc, path, params, query)
                else:
                    insert_list_type(self.conn, url, 0,
                                     'rdef_web_blacklist', scm)
        elif(link_Status == 'WL'):  # Whitelist, forwarding connection
            print("\n[*] Whitelisted url forwarding")
            self.socket_connection(netloc, path, params, query)
        else:
            # Blacklist, Loading error page
            print("\n[!] Blacklisted url blocked")
            if self.load_blocked_page(url):
                self.socket_connection(netloc, path, params, query)

    def load_blocked_page(self, url, alert=False):
        if alert:
            self.icon.icon_notify(f'Detected suspicious activity in {url}')
            if self.icon.defend_state():
                self.send_error(403)
                self.close_connection = 1
                return False
            else:
                return True
        else:
            if self.icon.defend_state():
                self.send_error(403)
                self.close_connection = 1
            else:
                return True

    def socket_connection(self, netloc, path, params, query):
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            if self._connect_to(netloc, soc):
                self.log_request()
                text = "%s %s %s\r\n" % (
                    self.command,
                    urlunparse(('', '', path, params, query, '')),
                    self.request_version)
                soc.send(text.encode())
                self.headers['Connection'] = 'close'
                del self.headers['Proxy-Connection']
                for key_val in self.headers.items():
                    text = "%s: %s\r\n" % key_val
                    soc.send(text.encode())
                soc.send("\r\n".encode())
                self._read_write(soc)
        except Exception as e:
            self.logger_instance.write_log(172, 1, e)
        finally:
            soc.close()
            self.connection.close()

    def _read_write(self, soc, max_idling=50):
        try:
            iw = [self.connection, soc]
            ow = []
            count = 0
            while 1:
                count += 1
                (ins, _, exs) = select.select(iw, ow, iw, 3)
                if exs:
                    break
                if ins:
                    for i in ins:
                        if i is soc:
                            out = self.connection
                        else:
                            out = soc
                        data = None
                        try:
                            data = i.recv(8192)
                        except Exception as e:
                            self.logger_instance.write_log(170, 1, e)
                        if data:
                            out.send(data)
                            count = 0
                else:
                    pass
                if count == max_idling:
                    break
        except Exception as e:
            self.logger_instance.write_log(171, 1, e)

    def do_CONNECT_read_write(self, address):
        try:
            s = socket.create_connection(address, timeout=self.timeout)
            print("\n[*] Socket created")
        except Exception as e:
            self.send_error(502)
            print(e)
            return
        self.send_response(200, 'Connection Established')
        self.end_headers()

        conns = [self.connection, s]
        self.close_connection = 0
        while not self.close_connection:
            rlist, wlist, xlist = select.select(
                conns, [], conns, self.timeout)
            if xlist or not rlist:
                break
            for r in rlist:
                other = conns[1] if r is conns[0] else conns[0]
                data = None
                try:
                    data = r.recv(8192)
                except Exception as e:
                    self.logger_instance.write_log(170, 1, e)
                if not data:
                    self.close_connection = 1
                    break
                other.sendall(data)

    def do_POST(self, body=True):
        self.do_GET()

    def do_CONNECT(self):
        address = self.path.split(':', 1)
        url = ''
        if(address[0] == 'http'):
            address = [self.path.split('://')[1], 80]
            # print(address)
            url = 'http://' + address[0]
            protocol = 'http'
        else:
            address[1] = int(address[1]) or 443
            url = address[0]
            url = "https://" + url
            protocol = 'https'
        link_Status = isurlindb(self.conn, url)
        if(link_Status == 'CHECK'):
            status = self.checkUrl(url)

            if(status):
                inserturl(self.conn, 0, url, 0, 0, 0, protocol)
                insert_list_type(self.conn, url, 0,
                                 'rdef_web_whitelist', protocol)
                print("\n[*] Harmless url forwarding")
                self.do_CONNECT_read_write(address)
            else:
                # print("Malicious")
                print("\n[!] Malicious url blocked")
                # Insert checked and malicious link to blacklist
                insert_list_type(self.conn, url, 0,
                                 'rdef_web_blacklist', protocol)
                if self.load_blocked_page(url, alert=True):
                    self.do_CONNECT_read_write(address)

        elif(link_Status == 'WL'):
            print("\n[*] Whitelisted url forwarding")
            self.do_CONNECT_read_write(address)
        else:
            # TODO: Blacklisted url handling
            print("\n[!] Blacklisted url blocked")
            if self.load_blocked_page(url):
                self.do_CONNECT_read_write(address)

    def send_resp_headers(self, resp):
        try:
            respheaders = resp.headers
            for key in respheaders:
                if key not in ['Content-Encoding', 'Transfer-Encoding', 'content-encoding', 'transfer-encoding', 'content-length', 'Content-Length']:
                    self.send_header(key, respheaders[key])
            self.send_header('Content-Length', len(resp.content))
            self.end_headers()
        except Exception as e:
            self.logger_instance.write_log(173, 1, e)

    def checkUrl(self, url):
        # Creating a web request to VirusTotal API
        url = base64.urlsafe_b64encode(url.encode()).decode().strip("=")
        vt_full_url = self.api_url + "urls/{}".format(url)
        parameters = {"x-apikey": self.api_key}
        response = requests.get(vt_full_url, headers=parameters)
        if(response.status_code == 200):
            # VT successfull request
            responseData = json.loads(response.text)
            harmless, malicious, suspicious, timeout, undetected = self.vt_response_parser_instance.last_analysis_stats(
                responseData)
            #malicious = 5
            if (malicious > 0):
                # Writing to log that malicious site detected
                print('[!] {} Agents found this url malicious'.format(malicious))
                self.logger_instance.write_log(90, 2)
                return False
            else:
                return True
        else:
            print('[!] Bad VT request\n')
            return True
