from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = "Hello Mufkr"
app.config['TEMP_MEDIA_PATH'] = "/Media/Pending Upload"
app.config['PERM_MEDIA_PATH'] = "/Media"

from srvCore import routes