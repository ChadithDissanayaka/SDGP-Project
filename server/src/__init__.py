from flask import Flask
from flask_cors import CORS


from src.controllers.authController import authCtrl 
from src.ml_modal.modalController import mlCtrl

app = Flask(__name__)
cors = CORS(app)


app.register_blueprint(authCtrl, url_prefix='/auth')
app.register_blueprint(mlCtrl, url_prefix='/ml')
