from http.server import BaseHTTPRequestHandler
import urllib
from threading import Thread
import time


from splitwise import Splitwise

host_name = "localhost"
server_port = 6969

CONSUMER_KEY = "Nv4qPOn67amh43oqVgl5DQOBaBAbL1QhZKPpG9au"
CONSUMER_SECRET = "H6T11tOVJJxS3Sgjc66wLEeZVCH8701i2BaLwNAJ"
AUTH_TIMEOUT_S = 30

class postCounter(object):

    def __init__(self):
        self.num_posts = 0

    def increment(self):
        self.num_posts += 1

class Keychain(object):
    # Store authentication secrets

    def __init__(self):
        self.keys = {}


    def get_secret(self, name):

        secret = None
        if name in self.keys.keys():
            secret = self.keys[name]

        return secret

    def add_secret(self, name, key):

        # Check for existing keys
        if name in self.keys.keys():
            raise ValueError("A secret for {} is already in the keychain!".format(name))

        # Add key to keychain
        self.keys[name] = key
        return



class Housemates(BaseHTTPRequestHandler):

    counter = postCounter()
    keychain = Keychain()
    sw_client = Splitwise(CONSUMER_KEY, CONSUMER_SECRET)

    homepage = "http://{}:{}".format(host_name, server_port)

    def request_splitwise_auth(self, consumer_key, consumer_secret):
        """ Authorize this object with Splitwise

        """

        # Begin authentication
        #state = "splitwise"
        url, state = self.sw_client.getOAuth2AuthorizeURL(self.homepage)

        print("Please authorize integration with Splitwise: {}".format(url))

        return

        # Wait for authentication
        t_start = time.time()
        while (self.keychain.get_secret(state) is None):
            time.sleep(1.0)

            # Check for Timeout
            t_elapsed = time.time() - t_start
            if t_elapsed > AUTH_TIMEOUT_S:
                raise TimeoutError("Splitwise authentication took more than {} s!".format(AUTH_TIMEOUT_S))


    def complete_splitwise_auth(self, state):

        code = self.keychain.get_secret(state)
        redirect_uri = self.homepage

        # Mock splitwise implementation
        data = "client_id=%s&client_secret=%s&grant_type=authorization_code&code=%s&redirect_uri=%s" % (
            CONSUMER_KEY, CONSUMER_SECRET, code, redirect_uri)

        OAUTH_BASE_URL = "https://www.splitwise.com/"
        OAUTH2_TOKEN_URL = OAUTH_BASE_URL + "oauth/" \
                "token"

        url = Splitwise.OAUTH2_TOKEN_URL
        method = 'POST'


        auth = None
        from requests import Request, sessions

        requestObj = Request(method=method, url=url, data=data, auth=auth, files=None)

        prep_req = requestObj.prepare()

        with sessions.Session() as session:
            response = session.send(prep_req)

        import pdb; pdb.set_trace()


        # Get access token
        access_token = self.sw_client.getOAuth2AccessToken(self.keychain.get_secret(state), self.homepage)
        self.sw_client.setOAuth2AccessToken(access_token)
        print("Access Token: {}".format(access_token))

        # Verify Access
        import pdb; pdb.set_trace()


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
        elif res.path.startswith("/authorization"):

            # Redirect to homepage
            self.send_response(301)
            self.send_header("Location", self.homepage)
            self.end_headers()

            # Complete splitwise authentication
            params = urllib.parse.parse_qs(res.query)
            self.keychain.add_secret(params['state'][0], params['code'][0])
            self.complete_splitwise_auth(params['state'][0])


    def do_POST(self):

        length = int(self.headers['Content-Length'])
        post_data = urllib.parse.parse_qs(self.rfile.read(length).decode('utf-8'))
        print("Got Post!")
        print(post_data)

        self.counter.num_posts += 1

        self.request_splitwise_auth(CONSUMER_KEY, CONSUMER_SECRET)
        #auth_thread = Thread(target = self.authorize_splitwise, args=(CONSUMER_KEY, CONSUMER_SECRET))
        #auth_thread.start()
        #auth_thread.join()
        #print("Auth thread finished ... exiting")




