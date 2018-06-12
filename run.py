from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY']= 'apalah-disini-ceritanya'
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.config['PROPAGATE_EXCEPTIONS'] = True

cors = CORS(app, resources={r"/api/*":{"origins":"*"}})





db = SQLAlchemy(app)
api = Api(app)
jwt = JWTManager(app)

@app.before_first_request
def create_tables():
    db.create_all()


import views, models, resources

@jwt.token_in_blacklist_loader
def check_token(decrypted_token):
    jti = decrypted_token['jti']
    return models.RevokedTokenModel.is_jti_blacklisted(jti)

api.add_resource(resources.UserRegistration, '/api/registration')
api.add_resource(resources.UserLogin, '/api/login')
api.add_resource(resources.UserLogoutAccess, '/api/logout/access')
api.add_resource(resources.UserLogoutRefresh, '/api/logout/refresh')
api.add_resource(resources.TokenRefresh, '/api/token/refresh')
api.add_resource(resources.AllUsers, '/api/users')
api.add_resource(resources.SecretResource, '/api/secret')