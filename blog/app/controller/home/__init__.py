from flask import Flask
from flask import Blueprint
app = Flask(__name__)
home = Blueprint('home', __name__)
from .home import *