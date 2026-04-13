def test_login_success(client, sample_user):
    response = client.post('/login', json={
        'username': 'testuser',
        'password': 'password123'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert 'access_token' in data
    assert data['id'] == sample_user.id

def test_login_wrong_password(client, sample_user):
    response = client.post('/login', json={
        'username': 'testuser',
        'password': 'wrongpassword'
    })
    assert response.status_code == 401
    assert response.get_json()['message'] == 'Invalid credentials'

def test_login_missing_username(client):
    response = client.post('/login', json={'password': 'password123'})
    assert response.status_code == 400
    assert 'Missing username' in response.get_json()['message']

def test_login_missing_password(client):
    response = client.post('/login', json={'username': 'testuser'})
    assert response.status_code == 400
    assert 'Missing password' in response.get_json()['message']

def test_login_nonexistent_user(client):
    response = client.post('/login', json={
        'username': 'nobody',
        'password': 'password123'
    })
    assert response.status_code == 401

def test_refresh_token(client, auth_headers):
    response = client.post('/refresh', headers=auth_headers)
    assert response.status_code == 200
    assert 'access_token' in response.get_json()

def test_refresh_without_token(client):
    response = client.post('/refresh')
    assert response.status_code == 401

def test_logout(client, auth_headers):
    response = client.post('/logout', headers=auth_headers)
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Successfully logged out'

def test_token_revoked_after_logout(client, auth_headers):
    # logout first
    client.post('/logout', headers=auth_headers)
    # then try to use the same token
    response = client.post('/refresh', headers=auth_headers)
    assert response.status_code == 401