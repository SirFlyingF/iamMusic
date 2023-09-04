from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = "Hello Mufkr"
app.config['MEDIA_PATH'] = "Media/"

from srvCore import routes