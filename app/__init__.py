from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flasgger import Swagger

db = SQLAlchemy()
migrate = Migrate()

# In-memory token blocklist (replace with Redis for production)
token_blocklist = set()

def create_app(config=None):
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    if config:
        app.config.update(config)

    jwt = JWTManager(app)
    db.init_app(app)
    migrate.init_app(app, db)
    Swagger(app)
    CORS(app)

    # Wire up the token blocklist check
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        jti = jwt_payload['jti']
        return jti in token_blocklist

    from app.routes.transaction import transaction
    from app.routes.user import user
    from app.routes.auth import auth
    from app.routes.main import main

    app.register_blueprint(transaction)
    app.register_blueprint(user)
    app.register_blueprint(auth)
    app.register_blueprint(main)

    return app