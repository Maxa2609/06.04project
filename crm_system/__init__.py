from flask import Flask

app = Flask(__name__)

from crm_system import routes
