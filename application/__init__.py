from flask import Flask
from config import Config
# from flask_mongoengine import MongoEngine

app = Flask(__name__, static_folder='static')
app.config.from_object(Config)

# db = MongoEngine()
# db.init_app(app)

from application import routes
# from application import sandbox
