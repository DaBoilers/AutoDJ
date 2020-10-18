from flask import Flask, redirect, request
from urllib.parse import quote
from google.cloud import vision
import os
import base64

app = Flask(__name__)
likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                   'LIKELY', 'VERY_LIKELY')
# Spotify Config
CLIENT_ID = os.environ['SPOTIFY_CLIENT_ID']
SCOPES = ['streaming']
REDIRECT_URI = 'http://localhost:5000/auth_callback'

@app.route('/')
def index(): 
    print('index')
    return None

# App endpoints
@app.route('/user_image', methods=["GET", "POST"])
def user_image():
    data = request.get_json().content
    encoded_data = base64.b64encode(data)
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=encoded_data)
    resp = client.face_detection(image=image)
    faces = resp.face_annotations

    for face in faces:
        print('anger: {}'.format(likelihood_name[face.anger_likelihood]))
        print('joy: {}'.format(likelihood_name[face.joy_likelihood]))
        print('surprise: {}'.format(likelihood_name[face.surprise_likelihood]))

    if resp.error.message:
        print(resp.error.message)

    return '<div>Test</div>'

# Spotify endpoints
@app.route('/auth')
def auth():
    return redirect('https://accounts.spotify.com/authorize' + 
                    '?response_type=code' + 
                    '&client_id=' + CLIENT_ID +
                    '&scope=streaming' +
                    '&redirect_uri=' + quote(REDIRECT_URI))

@app.route('/auth_callback', methods=["GET", "POST"])
def auth_callback():
    print(request.args.get("code"))


