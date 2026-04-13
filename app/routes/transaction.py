from flask import Blueprint, request, jsonify
from app.services import TransactionService
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import swag_from
from .swagger_specs import (
    get_transactions_by_user_id_spec,
    create_transaction_spec,
)

transaction = Blueprint('transaction', __name__)

@transaction.route('/transactions/user/<int:user_id>', methods=['GET'])
@jwt_required()
@swag_from(get_transactions_by_user_id_spec)
def get_transactions_by_user_id(user_id):
    current_user_id = int(get_jwt_identity())
    if current_user_id != user_id:
        return jsonify({"message": "Unauthorized"}), 403
    transactions = TransactionService.get_all_by_user_id(user_id)
    return jsonify(transactions), 200

@transaction.route('/transactions', methods=['POST'])
@jwt_required()
@swag_from(create_transaction_spec)
def create_transaction():
    data = request.get_json()
    return TransactionService.create_transaction(data)

@transaction.route('/transactions/user/<int:user_id>/between', methods=['GET'])
@jwt_required()
def get_transactions_by_user_id_between_dates(user_id):
    current_user_id = int(get_jwt_identity())
    if current_user_id != user_id:
        return jsonify({"message": "Unauthorized"}), 403
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    if not start_date:
        start_transaction = TransactionService.get_first_transaction_by_user_id(user_id)
        start_date = start_transaction['at_date']
    if not end_date:
        end_transaction = TransactionService.get_last_transaction_by_user_id(user_id)
        end_date = end_transaction['at_date']
    transactions = TransactionService.get_all_by_user_id_between_dates(user_id, start_date, end_date)
    return jsonify(transactions), 200