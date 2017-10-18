from flask import Flask



app = Flask(__name__)
app.config.from_object('config')
# app.config['DATA_PATH'] = DATA_PATH

from app import views
