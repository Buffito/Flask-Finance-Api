from app.models import Transaction, TransactionType, User
from app import db
from app.schemas import TransactionSchema
from marshmallow import ValidationError
from datetime import datetime
from flask import jsonify

class TransactionService:   
    @staticmethod
    def get_all_by_user_id(user_id):
        transactions = Transaction.query.filter_by(user_id=user_id).order_by(Transaction.at_date.desc()).all()
        return TransactionSchema(many=True).dump(transactions)

    @staticmethod
    def get_last15_by_user_id(user_id):
        transactions = Transaction.query.filter_by(user_id=user_id).order_by(Transaction.at_date.desc()).limit(15).all()
        return TransactionSchema(many=True).dump(transactions)
    
    @staticmethod
    def create_transaction(data):
        schema = TransactionSchema()
        print(data)
        try:
            validated_data = schema.load(data)
        except ValidationError as err:
            return jsonify(err.messages), 400

        transaction_type_id = validated_data['transaction_type']['id']
        transaction_type = TransactionType.query.get(transaction_type_id)
        if not transaction_type:
            return jsonify({"error": "Invalid transaction type ID"}), 400

        user = User.query.get(validated_data['user_id'])
        if not user:
            return jsonify({"error": "Invalid user ID"}), 400

        transaction = Transaction(
            type_id=transaction_type.id, 
            amount=validated_data['amount'],
            at_date=validated_data['at_date'], 
            user_id=user.id
        )
        
        try:
            db.session.add(transaction)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400
        
        return jsonify(TransactionSchema().dump(transaction)), 201
    
    @staticmethod
    def get_all_by_user_id_between_dates(user_id, start_date, end_date):
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        transactions = Transaction.query.filter(
            Transaction.user_id == user_id,
            Transaction.at_date >= start_date,
            Transaction.at_date <= end_date
        ).all()
        return [transaction.to_dict() for transaction in transactions]
    
    @staticmethod
    def get_first_transaction_by_user_id(user_id):
        transaction = Transaction.query.filter_by(user_id=user_id).first()
        return TransactionSchema().dump(transaction)
    
    @staticmethod
    def get_last_transaction_by_user_id(user_id):
        transaction = Transaction.query.filter_by(user_id=user_id).order_by(Transaction.id.desc()).first()
        return TransactionSchema().dump(transaction)