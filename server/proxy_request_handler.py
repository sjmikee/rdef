import socket
import select
import requests
import json
import base64
import os
from urllib.parse import urlparse, urlunparse
from http.server import BaseHTTPRequestHandler
from config.setsqlite import get_connection, isurlindb, insert_list_type, inserturl
import config.main_config as main_config
import config.resources as resources
from server.local_file_adapter import LocalFileAdapter
import server.vt_response_parser as vt_response_parser
import logger.logger as logger

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


    def load_blocked_page(self):
        try:
            #print("hey")
            response = requests.get('https://www.google.com')
            print(response.text)

            self.send_response(301)
            self.send_header('Location', 'https://www.google.com')
            self.end_headers()
            self.do_GET()
            #self.do_CONNECT()
            respi = response.text.encode()
            self.wfile.write(respi)            
            #return
        except Exception as e:
            print(e)


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
<<<<<<< HEAD
            status = self.checkUrl(url)
            if(status):
                print("[*] Harmless url forwarding")
=======
            if(self.checkUrl(url)):
                print("\n[*] Harmless url forwarding")
>>>>>>> 2a8bfbd6826e635d4354e8878723cb5feeb0629e
                self.socket_connection(netloc, path, params, query)
                inserturl(self.conn, self.path, 0, 0, 0,
                          0, 0)  # Insert to DB whitelist
                insert_list_type(self.conn, url, 0, 'whitelist')
            else:  # Malicious, inserting to DB
                print("\n[!] Malicious url blocked")
                # Insert checked and malicious link to blacklist
                insert_list_type(self.conn, url, 0, 'blacklist')
                self.load_blocked_page()
        elif(link_Status == 'WL'):  # Whitelist, forwarding connection
            print("\n[*] Whitelisted url forwarding")
            self.socket_connection(netloc, path, params, query)
        else:
<<<<<<< HEAD
            # Blacklist, Loading error page, returned error from DB that we BL
            print("[!] Blacklisted url blocked")
=======
            # Blacklist, Loading error page
            print("\n[!] Blacklisted url blocked")
>>>>>>> 2a8bfbd6826e635d4354e8878723cb5feeb0629e
            self.load_blocked_page()

<<<<<<< HEAD


=======
    def load_blocked_page(self):
        try:
            print("Loading stuff")
            #requests_session = requests.session()
            #requests_session.mount('file:///', LocalFileAdapter)
            # print(resources_instance.url_blocked_file())
            #resp = requests_session.get(resources_instance.url_blocked_file())
            # resp.status_code
            # resp.text
            #s = TestSession()
            #s.mount('http://github.com/about/', TestAdapter(b'github.com/about'))
            #r = s.get('http://github.com/about/')
            # print(r.text)
            # r.text
            # self.send_response(r.status_code)

            #requests_session = requests.session()
            #requests_session.mount('file://', LocalFileAdapter())
            #resp = requests_session.get('file://C:/Users/Kobi/Desktop/Dev/rdef/resources/url_blocked.html')
            # print(resp)
            resppp = '''<html>
<head>
    <title>MALICIOUS URL BLOCKED</title>
</head>
<body>
    <center>
        <h1>********* BLOCKED *********<br></h1>
        <h3>Realtime VirusTotal defender has blocked a malicious url<br>You are safe</h3>
    </center>
</body>
</html>'''
            resppp = resppp.encode()
            # self.send_response(200)
            #self.send_header("Content-type", "text/html")
            # self.end_headers()
            self.send_response(302)
            self.send_header(
                'Location', 'https://www.google.com/logos/doodles/2020/thank-you-coronavirus-helpers-april-25-26-6753651837108777-s.png')
            self.end_headers()
            # self.send_response(200)
            # self.send_resp_headers(r)
            # self.send_resp_headers(''.encode())
            # self._read_write(resp)
            # self.wfile.write(resppp)
            # self.wfile.write(resppp)             #YOU Can change to resppp to get what you wanted, the issue is that it kinda detects
            # a new connect_to request while handling this one, and raise basehttp handle_http_one request flush on a closed file

            self.flush_headers()
            self.close_connection = 1
            self.connection.sendall(''.encode())
            # self.finish
        except Exception as e:
            print(e)
>>>>>>> 35d752bb0fcb241552557f3600b71ccd346dc8d8

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
<<<<<<< HEAD
            #print("\t" "bye")
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
=======
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
>>>>>>> 2a8bfbd6826e635d4354e8878723cb5feeb0629e


    def do_POST(self, body=True):
        self.do_GET()


    def do_CONNECT(self):
        address = self.path.split(':', 1)
        url = ''
        if(address[0] == 'http'):
            address = [self.path.split('://')[1], 80]
            # print(address)
            url = 'http://' + address[0]
        else:
            address[1] = int(address[1]) or 443
            url = address[0]
            url = "https://" + url
        link_Status = isurlindb(self.conn, url)
        if(link_Status == 'CHECK'):
            status = self.checkUrl(url)

            if(status):
                inserturl(self.conn, url, 0, 0, 0, 0, 0)
                insert_list_type(self.conn, url, 0, 'whitelist')
                print("\n[*] Harmless url forwarding")
                try:
                    s = socket.create_connection(address, timeout=self.timeout)
<<<<<<< HEAD
                    #print("socket created")
=======
                    print("\n[*] Socket created")
>>>>>>> 2a8bfbd6826e635d4354e8878723cb5feeb0629e
                except Exception as e:
                    self.send_error(502)
                    #print(e)
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
            else:
                # print("Malicious")
                print("\n[!] Malicious url blocked")
                # Insert checked and malicious link to blacklist
                insert_list_type(self.conn, url, 0, 'blacklist')
                self.load_blocked_page()

        elif(link_Status == 'WL'):
            print("\n[*] Whitelisted url forwarding")
            try:
                s = socket.create_connection(address, timeout=self.timeout)
                print("\n[*] Socket created")
            except Exception as e:
                self.send_error(502)
                #print(e)
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
        else:
<<<<<<< HEAD
            # No need to enter to DB cause we got BL, means already in blacklist.
            print("[!] Blacklisted url blocked")
=======
            # TODO: Blacklisted url handling
            print("\n[!] Blacklisted url blocked")
>>>>>>> 2a8bfbd6826e635d4354e8878723cb5feeb0629e
            self.load_blocked_page()


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
        print("we are making url ceck via virus total")
        rawurl = url
        url = base64.urlsafe_b64encode(url.encode()).decode().strip("=")
        vt_full_url = self.api_url + "urls/{}".format(url)
        parameters = {"x-apikey": self.api_key}
        response = requests.get(vt_full_url, headers=parameters)
        print(response)
        print(response.status_code)
        if(response.status_code == 200):
            # VT successfull request
            responseData = json.loads(response.text)
            harmless, malicious, suspicious, timeout, undetected = self.vt_response_parser_instance.last_analysis_stats(
                responseData)
            print(malicious)
            print("we entered malicious section")
            print(rawurl)
            if ("cern" in rawurl):
                print("test test test",url)
                malicious = 6 #blocking cern

            if (malicious > 0):
<<<<<<< HEAD
                # Writing to log that malicious site detected malicious returns false
=======
                # Writing to log that malicious site detected
                print('[!] {} Agents found this url malicious'.format(malicious))
>>>>>>> 2a8bfbd6826e635d4354e8878723cb5feeb0629e
                self.logger_instance.write_log(90, 2)
                return False
            else:
                return True
        else:
<<<<<<< HEAD
=======
            print('[!] Bad VT request\n')
>>>>>>> 2a8bfbd6826e635d4354e8878723cb5feeb0629e
            return True

