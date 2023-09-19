import os

from flask import Flask, request, jsonify, render_template, redirect, url_for,send_file
from faker import Faker
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import SyncGrant
from werkzeug.utils import secure_filename

app = Flask(__name__)
fake = Faker()


@app.route('/')
def index():
    return render_template('index.html')

# Add your Twilio credentials
@app.route('/token')
def generate_token():
    TWILIO_ACCOUNT_SID = 'AC63815614e3354ef31fda26179754b228'
    TWILIO_SYNC_SERVICE_SID = 'IS844b37fa51a7389846daf0a5406edc8d'
    TWILIO_API_KEY = 'SK5a94cb1147beeff9134676dd7d253a42'
    TWILIO_API_SECRET = '0zoRfNMf2uOaiOmOA0OV73fAAJRiFENz'

    username = request.args.get('username', fake.user_name())

    # create access token with credentials
    token = AccessToken(TWILIO_ACCOUNT_SID, TWILIO_API_KEY, TWILIO_API_SECRET, identity=username)
    # create a Sync grant and add to token
    sync_grant_access = SyncGrant(TWILIO_SYNC_SERVICE_SID)
    token.add_grant(sync_grant_access)
    return jsonify(identity=username, token=token.to_jwt().decode())

# Write the code here
@app.route('/', methods=['POST'])
def download_text():
    text_from_Notepad = request.form['text']
    with open('workfile.txt', 'w') as f:
        f.write(text_from_Notepad)

    path_to_store_doc = 'workfile.txt'
    
    return send_file(path_to_store_doc, as_attachment=True)


if __name__ == "__main__":
    app.run(host='localhost', port='5001', debug=True)
