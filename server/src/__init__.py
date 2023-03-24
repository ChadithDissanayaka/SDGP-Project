from flask import Flask
from flask_cors import CORS


from src.controllers.authController import authCtrl 

app = Flask(__name__)
cors = CORS(app)


app.register_blueprint(authCtrl, url_prefix='/auth')
