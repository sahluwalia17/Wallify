import pyrebase
import json

config = {
	"apiKey": None,
    "authDomain": "wallify-bea20.firebaseapp.com",
    "databaseURL": "https://wallify-bea20.firebaseio.com",
    "projectId": "wallify-bea20",
    "storageBucket": "wallify-bea20.appspot.com",
    "messagingSenderId": "974113509801"
}

with open ("config.txt") as f:
	apiKey = str(f.readline())
	config["apiKey"] = apiKey

fb = pyrebase.initialize_app(config)

authentication = fb.auth()

email = input("Please enter an email\n");
password = input("Please enter password\n");
#user = authentication.create_user_with_email_and_password(email, password);

#TODO: IMPLEMENT TRY CATCHES TO CATCH DIFFERENT SCENARIOS
#1) WRONG PASSWORD (SIGNIN PAGE)
#2) LOGIN ALREADY EXISTS (SIGNUP PAGE)
#3) LOGIN DOESN'T EXIST (SIGNIN PAGE) I THINK?
#4) WEAK PASSWORD
#5) INVALID EMAIL

#this is the signup page
try:
	user = authentication.create_user_with_email_and_password(email,password)
	#refactor template to go to wallify page
except Exception as e:
	get_error = e.args[1]
	error = json.loads(get_error)['error']
	#print(error['message'])
	msg = error['message']
	print (msg)
	invalid = "Please enter a valid email"
	weak = "Password length must be at least 6 characters"
	exist = "This email is already in use"
	if msg == "INVALID_EMAIL":
		pass
		#reload the page with a header this is done in html
	elif "WEAK_PASSWORD" in msg:
		pass
	elif msg == "EMAIL_EXISTS"

#authentication.get_account_info(user['idToken'])
#print(user)

