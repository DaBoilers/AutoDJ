from flask import Flask, redirect, request
from urllib.parse import quote
from urllib.request import urlretrieve
from google.cloud import vision
import os

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
@app.route('/user_image', methods=['POST', 'OPTIONS'])
def user_image():
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
            'Access-Control-Max-Age': 1000,
            'Access-Control-Allow-Headers': 'origin, x-csrftoken, content-type, accept',
        }
        return '', 200, headers

    filename, m = urlretrieve(request.get_json()['content']) 
    data = open(filename,'rb').read()
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=data)
    resp = client.face_detection(image=image)
    faces = resp.face_annotations

    for face in faces:
        print('anger: {}'.format(likelihood_name[face.anger_likelihood]))
        print('joy: {}'.format(likelihood_name[face.joy_likelihood]))
        print('surprise: {}'.format(likelihood_name[face.surprise_likelihood]))
        print('sorrow: {}'.format(likelihood_name[face.sorrow_likelihood]))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in face.bounding_poly.vertices])

        print('face bounds: {}'.format(','.join(vertices)))


    if resp.error.message:
        print(resp.error.message)
    return "<div>test</div>"

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


