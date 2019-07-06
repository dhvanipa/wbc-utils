import pyrebase
import firebase_admin
from firebase_admin import credentials, firestore

config = {
    "apiKey": "AIzaSyCwgogOI0rJDijj-r97dbWjEinKkrBH1Ok",
    "authDomain": "daydesign-a277f.firebaseapp.com",
    "databaseURL": "https://daydesign-a277f.firebaseio.com",
    "storageBucket": "daydesign-a277f.appspot.com"
}

# pyrebase auth config
# Get a reference to the auth service
firebase = pyrebase.initialize_app(config)

authe = firebase.auth()

# firestore config
# Use a service account
cred = credentials.Certificate('../serviceAccount.json')
firebase_admin.initialize_app(cred)

db = firestore.client()
