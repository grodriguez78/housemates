# Standard Libraries
from http.server import HTTPServer

from .context import housemates


def test_app(capsys, example_fixture):
    # pylint: disable=W0612,W0613

    host_name = "localhost"
    server_port = 8000

    web_server = HTTPServer((host_name, server_port), housemates.Housemates)    # noqa: F841
    print("Test server started http://{}:{}".format(host_name, server_port))

    # TODO: Run test server
    # Run server for 5s
    # start = time()
    # while(time() - start < 5.0):
    #     web_server.serve_forever()

    # web_server.server_close()
