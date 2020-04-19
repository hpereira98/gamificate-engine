from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin
import logging
from logging.handlers import SMTPHandler
from flask_mail import Mail
from flask_jwt_extended import JWTManager
from flasgger import Swagger


app = Flask(__name__, instance_relative_config=True) 
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
mail = Mail(app)

jwt = JWTManager(app)

from app.errors import bp as errors_bp
app.register_blueprint(errors_bp)

from app.auth import bp as auth_bp
app.register_blueprint(auth_bp, url_prefix='/auth')

from app.main import bp as main_bp
app.register_blueprint(main_bp)

from app.realms import bp as realms_bp
app.register_blueprint(realms_bp)

from app.api import bp as api_bp
app.register_blueprint(api_bp, url_prefix='/api')


# Error handling
if not app.debug:
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='Gamificate Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

## API DOC
app.config['SWAGGER'] = {
    'title': "Gamificate API",
    'uiversion': 3,
    # 'openapi': '3.0.2',
}
swagger_config = {
    'headers': [],
    'specs': [
        {
            'endpoint': 'docs',
            'route': '/swagger.json',
            'rule_filter': lambda rule: True,
            'model_filter': lambda tag: True
        }
    ],
    'static_url_path': '/flasgger_static',
    'swagger_ui': True,
    'specs_route': "/api/"
}
template = {
  "info": {
    "title": "Gamificate API",
    "description": "API available for Gamificate users with, at least, one Realm created. If you are not registered user, you will not have access to this API.",
    "contact": {
      "responsibleOrganization": "Universidade do Minho",
      "responsibleDeveloper": "Henrique Pereira, Pedro Moreira, Sarah Silva",
      "email": "gamificate.engine@gmail.com",
    },
    # "termsOfService": "http://me.com/terms",
    "version": "0.0.1"
  },
#   "host": "gamificate-engine.com",  # overrides localhost:500
#   "basePath": "/api",  # base bash for blueprint registration
  "schemes": [
    "http",
    "https"
  ],
#   "operationId": "getmyData"
    "securityDefinitions": {
        "Bearer": {
            "description":"Where above says '(apiKey)' it should say '(JWT)', but this version of Swagger UI doesn't allow it and there is no support yet for Flask in the newer versions. So, for accessing the API a valid JWT token must be passed in all the queries in the 'Authorization' header. A valid JWT token (access_token) is generated by the API and retourned as answer of a call to the route /auth giving a valid Realm ID and API key or, when the previous expires, by /auth/refresh. This last one requires the refresh_token instead of the access_token. The following syntax must be used in the 'Authorization' header :\n\n  \tBearer <token>",
            "type": "apiKey",
            "name": "Authorization",
            "in": "header"
        }
    }       
}
swagger = Swagger(app, config=swagger_config, template=template)

from app import models
