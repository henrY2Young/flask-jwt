from flask import Flask
from flask import Blueprint
app = Flask(__name__)
admin = Blueprint('admin', __name__)
user = Blueprint('user', __name__)
from .admin import *
from .user import *