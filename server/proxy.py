from http.server import BaseHTTPRequestHandler, HTTPServer
import server.proxy_request_handler as handler
import server.threading_http_server as server
import logger.logger as logger


class Proxy():
    '''Class to make our proxy mechanism'''
    logger_instance = logger.logger()
    logger_instance.create_logger()

    def start_proxy(self, port=9999, protocol="HTTP/1.1", api_url='', api_key=''):
        try:
            print("[*] Realtime VirusTotal server started on port: {}".format(port))
            server_address = ('localhost', port)
            handler.ProxyRequestHandler.protocol_version = protocol
            # Also contains the SQL inits
            httpd = server.ThreadingHTTPServer(
                server_address, handler.ProxyRequestHandler)
            print('[*] Server is running')
            self.logger_instance.write_log(50, 1)
            httpd.serve_forever()
        except Exception as e:
            self.logger_instance.write_log(150, 0, e)
