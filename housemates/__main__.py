# Standard Libraries
from http.server import HTTPServer

# Module Libraries
from .app import Housemates

host_name = "localhost"
server_port = 6969

if __name__ == '__main__':

    web_server = HTTPServer((host_name, server_port), Housemates)
    print("Server started http://{}:{}".format(host_name, server_port))

    try:
        web_server.serve_forever()
    except KeyboardInterrupt:
        pass

    web_server.server_close()
    print("Application Stopped")
