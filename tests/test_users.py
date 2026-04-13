def test_register_success(client):
    response = client.post('/register', json={
        'username': 'newuser',
        'password': 'securepass'
    })
    assert response.status_code == 201
    assert 'created' in response.get_json()['message'].lower()

def test_register_duplicate_username(client, sample_user):
    response = client.post('/register', json={
        'username': 'testuser',  # already exists
        'password': 'password123'
    })
    assert response.status_code == 400

def test_register_password_too_short(client):
    response = client.post('/register', json={
        'username': 'shortpassuser',
        'password': '123'  # less than 6 chars
    })
    assert response.status_code == 400
    assert 'password' in str(response.get_json()).lower()

def test_register_missing_username(client):
    response = client.post('/register', json={'password': 'password123'})
    assert response.status_code == 400

def test_register_missing_password(client):
    response = client.post('/register', json={'username': 'nopassuser'})
    assert response.status_code == 400