from http.server import BaseHTTPRequestHandler, HTTPServer
import server.proxy_request_handler as handler
import server.threading_http_server as server
import logger.logger as logger
import socket
import asyncio
import threading


class Proxy():
    '''Class to make our proxy mechanism'''
    logger_instance = logger.logger()
    logger_instance.create_logger()

    def start_proxy(self, port=9999, protocol="HTTP/1.1"):
        try:
            print('[*] Starting admin channel')
            admin_channel_thread = threading.Thread(target=self.admin_channel)
            admin_channel_thread.start()
            print("[*] Realtime VirusTotal server started on port: {}".format(port))
            server_address = ('localhost', port)
            handler.ProxyRequestHandler.protocol_version = protocol
            # Also contains the SQL inits
            self.httpd = server.ThreadingHTTPServer(
                server_address, handler.ProxyRequestHandler)
            print('[*] Server is running')
            self.logger_instance.write_log(50, 1)
            self.httpd.serve_forever()
        except Exception as e:
            self.logger_instance.write_log(150, 0, e)

    def stop_proxy(self):
        print("[*] Stopping Server")
        self.httpd.socket.close()
        self.httpd.server_close()

    def admin_channel(self):
        async def handle_echo(reader, writer):
            data = await reader.read(100)
            message = data.decode()
            addr = writer.get_extra_info('peername')

            print(f"Received {message!r} from {addr!r}")
            if message == 'D4f{gb]@67gd#(Gdl;':
                reply = ''.join(chr(ord(a) ^ ord(b))
                                for a, b in zip(message, 'admin_channel_rdef'))
                print(f"Send: {reply!r}")
                writer.write(reply.encode())
                await writer.drain()

                print("Close the connection")
                writer.close()
            else:
                print("Close the connection")
                writer.close()

        async def main():
            server = await asyncio.start_server(
                handle_echo, '127.0.0.1', 8888)

            addr = server.sockets[0].getsockname()
            print(f'Admin channel on {addr}')

            async with server:
                await server.serve_forever()

        asyncio.run(main())
