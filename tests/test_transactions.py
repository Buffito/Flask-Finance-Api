def test_get_transactions_empty(client, auth_headers, sample_user):
    response = client.get(
        f'/transactions/user/{sample_user.id}',
        headers=auth_headers
    )
    assert response.status_code == 200
    assert response.get_json() == []

def test_get_transactions_returns_list(client, auth_headers, sample_user, sample_transaction):
    response = client.get(
        f'/transactions/user/{sample_user.id}',
        headers=auth_headers
    )
    data = response.get_json()
    assert response.status_code == 200
    assert len(data) == 1
    assert float(data[0]['amount']) == 100.00

def test_get_transactions_unauthorized(client, auth_headers, sample_user):
    other_user_id = sample_user.id + 999
    response = client.get(
        f'/transactions/user/{other_user_id}',
        headers=auth_headers
    )
    assert response.status_code == 403

def test_get_transactions_no_token(client, sample_user):
    response = client.get(f'/transactions/user/{sample_user.id}')
    assert response.status_code == 401

def test_create_transaction_success(client, auth_headers, sample_user, sample_transaction_type):
    payload = {
        'transaction_type': {'id': sample_transaction_type.id},
        'amount': 250.00,
        'at_date': '2024-03-01',
        'user_id': sample_user.id
    }
    response = client.post('/transactions', json=payload, headers=auth_headers)
    assert response.status_code == 201
    data = response.get_json()
    assert float(data['amount']) == 250.00

def test_create_transaction_invalid_type(client, auth_headers, sample_user):
    payload = {
        'transaction_type': {'id': 9999},  # non-existent type
        'amount': 100.00,
        'at_date': '2024-03-01',
        'user_id': sample_user.id
    }
    response = client.post('/transactions', json=payload, headers=auth_headers)
    assert response.status_code == 400

def test_create_transaction_invalid_user(client, auth_headers):
    payload = {
        'transaction_type': {'id': 1},
        'amount': 100.00,
        'at_date': '2024-03-01',
        'user_id': 9999  # non-existent user
    }
    response = client.post('/transactions', json=payload, headers=auth_headers)
    assert response.status_code == 400

def test_create_transaction_no_token(client, sample_user, sample_transaction_type):
    payload = {
        'transaction_type': {'id': sample_transaction_type.id},
        'amount': 100.00,
        'at_date': '2024-03-01',
        'user_id': sample_user.id
    }
    response = client.post('/transactions', json=payload)
    assert response.status_code == 401

def test_get_transactions_between_dates(client, auth_headers, sample_user, sample_transaction):
    response = client.get(
        f'/transactions/user/{sample_user.id}/between'
        f'?start_date=2024-01-01&end_date=2024-12-31',
        headers=auth_headers
    )
    assert response.status_code == 200
    assert len(response.get_json()) == 1

def test_get_transactions_between_dates_unauthorized(client, auth_headers, sample_user):
    response = client.get(
        f'/transactions/user/{sample_user.id + 999}/between'
        f'?start_date=2024-01-01&end_date=2024-12-31',
        headers=auth_headers
    )
    assert response.status_code == 403