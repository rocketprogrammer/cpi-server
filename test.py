# TestPeng1156:PamJam111!

from requests import session, post
import json, ssl, sys
from base64 import b64encode

def Register(username, password, nickname = None):
	if nickname == None: nickname = "dOte " + str(username)
	disney = session()
	__API__ = "https://registerdisney.go.com/jgc/v5/client/DI-CPREMIXAND.GC-PROD/api-key/"
	disney.headers["User-Agent"] = "Android Beany 1.0.9 Disney 2.0"

	SSL = ssl._create_unverified_context() # LATER?
	print 'Fetching API Auth...'
	API = disney.post(__API__, verify = False)
	API_KEY = API.headers["api-key"]

	disney.headers["Authorization"] = "APIKEY {0}".format(API_KEY)

	__CREATE__ = 'https://registerdisney.go.com/jgc/v5/client/DI-CPREMIXAND.GC-PROD/guest/register?langPref=en-US'
	__CHECK__ = 'https://registerdisney.go.com/jgc/v5/client/DI-CPREMIXAND.GC-PROD/validate/'

	disney.headers['X-Unity-Version'] = '5.4.3p1'
	disney.headers['Content-Type'] = 'application/json'
	disney.headers['Accept'] = 'application/json'

	CHECK_DATA = \
	{
		"email": username + "@vpsorg.top",
		"displayName": nickname,
		"username":username,
		"password":password
	}

	print "Checking username, password, nickname, and email"
	CHECK = disney.post(__CHECK__, data = json.dumps(CHECK_DATA))
	CHECK_REPLY = json.loads(CHECK.text)

	if CHECK_REPLY["error"] != None:
		print "Error authenticating Username or Password."
		print "Errors : ", map(lambda x: x["developerMessage"] ,CHECK_REPLY["error"]["errors"])
		return None

	CREATE_DATA = \
	{
		"password":password,
		"profile": \
		{
			"testProfileFlag":"N",
			"username":username,
			"firstName":"Flies",
			"lastName":None,
			"email":None,
			"parentEmail": username + "@vpsorg.top",
			"languagePreference":"en-US",
			"region":None
		},
		"marketing":[],
		"displayName":\
		{
			"proposedDisplayName" : nickname
		},
		"legalAssertions":["gtou_ppv2_proxy"]
	}

	print 'Registering...'
	CREATE = disney.post(__CREATE__, data = json.dumps(CREATE_DATA))
	CREATE_REPLY = json.loads(CREATE.text)

	if CREATE_REPLY["error"] != None:
		print "Error Registering account."
		print "Errors : ", map(lambda x: x["developerMessage"] ,CREATE_REPLY["error"]["errors"])
		return None

	return CREATE_REPLY
  
username = raw_input('Username: ')
password = raw_input('Password: ')
nickname = raw_input("Nickname: ")

REPLY = Register(username, password, nickname)
if REPLY == None:
	sys.exit(0)

PROFILE = REPLY["data"]["profile"]
print "Username:", PROFILE["username"]
print "Password:", password
print "SWID:", PROFILE["SWID"]
print "Session Key:", PROFILE["referenceId"]
print "Email:", PROFILE["parentEmail"]
print "Display Name Details:", REPLY["data"]["displayName"]
print "User Login Tokens:", REPLY["data"]["token"]
