
import json

import requests
from webob import Request

import vep
from repoze.who.plugins.vepauth.utils import sign_request

#  Hackery to use requsts module with WebOb Request object
HOST = "http://localhost:5000"
def do_request(req):
    return requests.get(HOST+req.path, headers=req.headers)

#  Make an BrowserID assertion to exchange for a token.
assertion = vep.DummyVerifier.make_assertion("test@example.com", HOST)
headers =  {"Authorization": "Browser-ID " + assertion}

#  Do the token exchange, we should get some OAuth credentials.
req = Request.blank("/request_token", headers=headers)
resp = do_request(req)
creds = json.loads(resp.content)
print ""
print "TOKEN IS:", creds
print ""

#  Now do a signed request, and see who we are
req = Request.blank("/whoami")
sign_request(req, **creds)
resp = do_request(req)
identity = json.loads(resp.content)
assert identity["username"] == "test@example.com"
print "YOU ARE:", identity["username"]
print ""


#  If we try to replay that request, the nonce will be rejected.
resp = do_request(req)
assert resp.status_code == 401

#  If we use bad credentials, we get a 401.
creds["oauth_consumer_secret"] = "EVILHACKER"
req = Request.blank("/whoami")
sign_request(req, **creds)
resp = do_request(req)
assert resp.status_code == 401

req = Request.blank("/")
sign_request(req, **creds)
resp = do_request(req)
assert resp.status_code == 401
