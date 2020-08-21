from flask import Flask
# Create app instance
app = Flask(__name__, template_folder='templates')
# MAIN DEPENDENCIES
from app import setup
from app import login
from app import creating
from app import reading
from app import updating
from app import deleting