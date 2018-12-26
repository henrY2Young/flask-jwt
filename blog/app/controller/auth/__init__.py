from flask import Flask
from flask import Blueprint
app = Flask(__name__)
auth = Blueprint('auth', __name__)
from .auth import *
