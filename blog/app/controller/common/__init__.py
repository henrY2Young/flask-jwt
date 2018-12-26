from flask import Flask
from flask import Blueprint
app = Flask(__name__)
common = Blueprint('common', __name__)
from .common import *