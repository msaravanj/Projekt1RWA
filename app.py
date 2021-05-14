from flask import Flask
from flask_restplus import Api
from controller._init_ import api

from model._init_ import db

app = Flask(__name__)

app.config.from_object('config.DevelopmentConfig')

db.init_app(app)
api.init_app(app)

if __name__ == '__main__':
    app.run(debug=True)