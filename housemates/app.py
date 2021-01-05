from http.server import BaseHTTPRequestHandler
import urllib
from threading import Thread
import time
import json

from splitwise import Splitwise

from .keychain import Keychain

host_name = "localhost"
server_port = 6969


class postCounter(object):

    def __init__(self):
        self.num_posts = 0

    def increment(self):
        self.num_posts += 1



class Housemates(BaseHTTPRequestHandler):

    counter = postCounter()
    keychain = Keychain()

    homepage = "http://{}:{}".format(host_name, server_port)

    def request_splitwise_auth(self):
        """ Authorize this object with Splitwise

        """

        CONSUMER_KEY, CONSUMER_SECRET = self.keychain.get_api_credentials("splitwise")
        sw_client = Splitwise(CONSUMER_KEY, CONSUMER_SECRET)

        # Begin authentication workflow
        url, state = sw_client.getOAuth2AuthorizeURL(self.homepage)
        print("Please authorize integration with Splitwise: {}".format(url))

        return


    def complete_splitwise_auth(self, state):

        # code = self.keychain.get_secret(state)
        # redirect_uri = self.homepage

        # # Mock splitwise implementation
        # data = "client_id=%s&client_secret=%s&grant_type=authorization_code&code=%s&redirect_uri=%s" % (
        #     CONSUMER_KEY, CONSUMER_SECRET, code, redirect_uri)

        # OAUTH_BASE_URL = "https://www.splitwise.com/"
        # OAUTH2_TOKEN_URL = OAUTH_BASE_URL + "oauth/" \
        #         "token"

        # url = Splitwise.OAUTH2_TOKEN_URL
        # method = 'POST'


        # auth = None
        # from requests import Request, sessions

        # requestObj = Request(method=method, url=url, data=data, auth=auth, files=None)

        # prep_req = requestObj.prepare()

        # with sessions.Session() as session:
        #     response = session.send(prep_req)

        # Instantiate Splitwise client
        CONSUMER_KEY, CONSUMER_SECRET = self.keychain.get_api_credentials("splitwise")
        sw_client = Splitwise(CONSUMER_KEY, CONSUMER_SECRET)

        # Get access token
        access_token = sw_client.getOAuth2AccessToken(self.keychain.get_secret(state), self.homepage)
        sw_client.setOAuth2AccessToken(access_token)
        print("Access Token: {}".format(access_token))

        # Verify Access
        import pdb; pdb.set_trace()

        # Record access token


    def do_GET(self):

        res = urllib.parse.urlparse(self.path)

        # Serve main page
        if res.path == "/":

            self.send_response(200)
            self.send_header("FooBar", "text/html")
            self.end_headers()

            self.wfile.write(bytes("<html><head><title>FooBar</title></head>".encode("utf-8")))
            self.wfile.write(bytes("<p># Post Requests: {}</p>".format(self.counter.num_posts).encode("utf-8")))
            self.wfile.write(bytes("<body>".encode("utf-8")))
            self.wfile.write(bytes("<p>This is an example web server.</p>".encode("utf-8")))
            self.wfile.write(bytes("</body></html>".encode("utf-8")))

        # Serve icon
        elif res.path.endswith(".ico"):
            pass

        # Handle Authentication Calls
        elif res.path.startswith("/authentication"):

            # Redirect to homepage
            self.send_response(301)
            self.send_header("Location", self.homepage)
            self.end_headers()

            # Complete splitwise authentication
            params = urllib.parse.parse_qs(res.query)
            self.keychain.add_secret(params['state'][0], params['code'][0])
            self.complete_splitwise_auth(params['state'][0])


    def do_POST(self):
        """ To run authentication, make a POST request to http://{homepage}/execute/authentication

        """


        self.counter.num_posts += 1

        # Check for commands
        if self.path.startswith("/execute"):

            self.send_response(200)

            workflow = self.path.split("/")[-1]
            self._run_workflow(workflow)

        else:
            self.send_response(400)

        # # Check content type
        # content_type = self.headers["Content-type"]
        # if content_type != "json":
        #     raise RuntimeError("Got Unsupported POST content type {}".format(content_type))

        # length = int(self.headers['Content-Length'])
        # post_data = json.loads(self.rfile.read(length).decode('utf-8'))


    def _run_workflow(self, workflow):
        """ Run prescripted workflows

        """

        # Run authentication workflows
        if workflow == "authentication":
            self.request_splitwise_auth()

        return





