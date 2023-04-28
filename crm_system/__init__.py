from flask import Flask
from flask_login import LoginManager
app = Flask(__name__)
app.secret_key = "some"
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)
from crm_system import routes
