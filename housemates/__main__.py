from .app import Housemates

from http.server import HTTPServer

from splitwise import Splitwise

CONSUMER_KEY = "GyueCC3JmIC8k7YLQPj0pETDLrqCsIP9wnqDwyZX"
CONSUMER_SECRET = "A17XLoj2cXOol17y2hSRjiDVLlwDa7LVkYgHjbYq"

host_name = "localhost"
server_port = 6969

if __name__ == '__main__':

    #app = Housemates()
    #app.authorize_splitwise(CONSUMER_KEY, CONSUMER_SECRET)
    #import pdb; pdb.set_trace()

    web_server = HTTPServer((host_name, server_port), Housemates)
    print("Server started http://{}:{}".format(host_name, server_port))


    try:
        web_server.serve_forever()
    except KeyboardInterrupt:
        pass

    web_server.server_close()
    print("Application Stopped")
