from dataclasses import dataclass
from datetime import datetime
from werkzeug.security import check_password_hash
from app import db
from sqlalchemy.orm import relationship

@dataclass
class TransactionType(db.Model):
    __tablename__ = 'transaction_types'
    
    id: int
    name: str
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    
    transactions = relationship('Transaction', back_populates='transaction_type')

    def __init__(self, name):
        self.name = name

@dataclass
class Transaction(db.Model):
    __tablename__ = 'transactions'
    
    id: int
    type_id: int
    amount: float
    at_date: datetime
    user_id: int
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type_id = db.Column(db.Integer, db.ForeignKey('transaction_types.id'), nullable=False)
    amount = db.Column(db.Numeric, nullable=False)
    at_date = db.Column(db.Date, nullable=False, default=datetime.today)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    transaction_type = relationship('TransactionType', back_populates='transactions')
    user = db.relationship('User', back_populates='transactions')
    
    def __init__(self, type_id, amount, at_date, user_id):
        self.type_id = type_id
        self.amount = amount
        self.at_date = at_date
        self.user_id = user_id
        
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'amount': float(self.amount),
            'date': self.at_date.strftime('%Y-%m-%d')
        }

@dataclass
class User(db.Model):
    __tablename__ = 'users'
    
    id: int
    username: str
    password: str
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    transactions = db.relationship('Transaction', back_populates='user')
    
    def __init__(self, username, password):
        self.username = username.strip()
        self.password = password.strip()

    @staticmethod
    def check_password(hashed_password, password):
        return check_password_hash(hashed_password, password)