from setsqlite import get_connection, isurlindb, insert_list_type, inserturl
from http.server import BaseHTTPRequestHandler
from local_file_adapter import LocalFileAdapter
import cfscrape
import socket
import select
import requests
import logger
import json
import main_config
import vt_response_parser
import base64
import os
import resources
from urllib.parse import urlparse, urlunparse

__config__file__ = 'config.rdef'
__working__directory__ = os.getcwd()
resources_instance = resources.resources()

class ProxyRequestHandler(BaseHTTPRequestHandler):
    logger_instance = logger.logger()
    config_instance = main_config.MainConfig()
    api_url, api_key = config_instance.read_configuration(__working__directory__, __config__file__)
    vt_response_parser_instance = vt_response_parser.vt_response_parser()
    protocol_version = 'HTTP/1.1'
    scraper = cfscrape.create_scraper()
    # Var
    conn = get_connection()  # Setting the SQL

    def do_HEAD(self):
        self.do_GET(body=False)

    def _connect_to(self, netloc, soc):
        i = netloc.find(':')
        if i >= 0:
            host_port = netloc[:i], int(netloc[i+1:])
        else:
            host_port = netloc, 80
        print("\t" "connect to %s:%d" % host_port)
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
        (scm, netloc, path, params, query, fragment) = urlparse(self.path, 'http')
        if scm != 'http' or fragment or not netloc:
            self.send_error(400, "bad url %s" % self.path)
            return
        print(scm, netloc, path)
        url = scm + '://' + netloc
        link_Status = isurlindb(self.conn, url)
        if(link_Status == 'CHECK'):
            if(self.checkUrl(url)):
                print("[*] Harmless url forwarding")
                self.socket_connection(netloc, path, params, query)
                inserturl(self.conn, self.path, 0, 0, 0, 0, 0)
                insert_list_type(self.conn, url, 0, 'whitelist')
            else:
                self.load_blocked_page()
                # Insert checked and malicious link to blacklist
                print("[!] Malicious url blocked")
                insert_list_type(self.conn, url, 0, 'blacklist')
        elif(link_Status == 'WL'):
            print("[*] Whitelisted url forwarding")
            self.socket_connection(netloc, path, params, query)
        else:
            print("[!] Blacklisted url blocked")
            self.load_blocked_page()

    def load_blocked_page(self):
        requests_session = requests.session()
        requests_session.mount('file://', LocalFileAdapter)
        resp = requests_session.get(resources_instance.url_blocked_file())
        self.send_response(resp.status_code)
        self.send_resp_headers(resp)
        self.wfile.write(resp.content)
        self.finish

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
        finally:
            print("\t" "bye")
            soc.close()
            self.connection.close()

    def _read_write(self, soc, max_idling=20):
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
                    data = i.recv(8192)
                    if data:
                        out.send(data)
                        count = 0
            else:
                print("\t" "idle", count)
            if count == max_idling:
                break

    def do_POST(self, body=True):
        return 0

    def do_CONNECT(self):
        address = self.path.split(':', 1)
        url = ''
        if(address[0] == 'http'):
            address = [self.path.split('://')[1], 80]
            print(address)
            url = 'http://' + address[0]
        else:
            address[1] = int(address[1]) or 443
            url = address[0]
            url = "https://" + url
        link_Status = isurlindb(self.conn, url)
        if(link_Status == 'CHECK'):
            if(self.checkUrl(url)):
                inserturl(self.conn, url, 0, 0, 0, 0, 0)
                insert_list_type(self.conn, url, 0, 'whitelist')
                print("[*] Harmless url forwarding")
                try:
                    s = socket.create_connection(address, timeout=self.timeout)
                    print("socket created")
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
                        data = r.recv(8192)
                        if not data:
                            self.close_connection = 1
                            break
                        other.sendall(data)
            else:
                # TODO: Malicious link handling
                pass

        elif(link_Status == 'WL'):
            print("[*] Whitelisted url forwarding")
            try:
                s = socket.create_connection(address, timeout=self.timeout)
                print("socket created")
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
                    data = r.recv(8192)
                    if not data:
                        self.close_connection = 1
                        break
                    other.sendall(data)
        else:
            # TODO: Blacklisted url handling
            print("[!] Blacklisted url blocked")

    def send_resp_headers(self, resp):
        respheaders = resp.headers
        for key in respheaders:
            if key not in ['Content-Encoding', 'Transfer-Encoding', 'content-encoding', 'transfer-encoding', 'content-length', 'Content-Length']:
                self.send_header(key, respheaders[key])
        self.send_header('Content-Length', len(resp.content))
        self.end_headers()

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
            if (malicious > 0):
                self.logger_instance.write_log(90, 2)
                return False
            else:
                return True
        else:
            print("hi")
            return False
