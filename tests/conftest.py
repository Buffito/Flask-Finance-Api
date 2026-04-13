# sets up the test app, in-memory database, and a client shared across all tests

import pytest
from app import create_app, db
from app.models import User, Transaction, TransactionType
from werkzeug.security import generate_password_hash
from datetime import date

@pytest.fixture(scope='session')
def app():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SECRET_KEY': 'test-secret',
        'JWT_SECRET_KEY': 'test-jwt-secret',
    })
    return app

@pytest.fixture(scope='function')
def db_session(app):
    with app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='function')
def client(app, db_session):
    return app.test_client()

@pytest.fixture
def sample_transaction_type(db_session):
    tt = TransactionType(name='Income')
    db.session.add(tt)
    db.session.commit()
    return tt

@pytest.fixture
def sample_user(db_session):
    user = User(
        username='testuser',
        password=generate_password_hash('password123', method='scrypt')
    )
    db.session.add(user)
    db.session.commit()
    return user

@pytest.fixture
def sample_transaction(db_session, sample_user, sample_transaction_type):
    transaction = Transaction(
        type_id=sample_transaction_type.id,
        amount=100.00,
        at_date=date(2024, 1, 15),
        user_id=sample_user.id
    )
    db.session.add(transaction)
    db.session.commit()
    return transaction

@pytest.fixture
def auth_token(client, sample_user):
    response = client.post('/login', json={
        'username': 'testuser',
        'password': 'password123'
    })
    return response.get_json()['access_token']

@pytest.fixture
def auth_headers(auth_token):
    return {'Authorization': f'Bearer {auth_token}'}