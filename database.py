import pyrebase

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
user = authentication.create_user_with_email_and_password(email, password);

authentication.get_account_info(user['idToken'])
print(user)

