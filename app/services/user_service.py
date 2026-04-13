from app.models import User
from app import db
from app.schemas import UserSchema
from marshmallow import ValidationError
from werkzeug.security import generate_password_hash
from flask import jsonify

class UserService:
    @staticmethod
    def create_user(user):
        schema = UserSchema()
        try:
            validated_data = schema.load(user)
        except ValidationError as err:
            return jsonify(err.messages), 400
        
        username = validated_data['username'].strip()
        password = validated_data['password'].strip()
            
        hashed_password = generate_password_hash(password, method="scrypt")
        new_user = User(username=username, password=hashed_password)
             
        try:
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400
        
        return jsonify({"message": "User created successfully!"}), 201
