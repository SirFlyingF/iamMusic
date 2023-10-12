from flask import Flask
from os import getenv

app = Flask(__name__)
app.config['MEDIA_PATH'] = "Media/"
app.config['SECRET_KEY'] = getenv('IAMM_API_KEY')
app.config['LOGLVL'] = int(getenv('IAMM_LOGLEVEL'))
app.config['LOG_PATH'] = getenv('IAMM_LOGFILE_PATH')

from srvCore import routes