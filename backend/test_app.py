import pytest
import os

# Устанавливаем базу в памяти ДО импорта приложения
os.environ['DATABASE_URL'] = 'sqlite:///:memory:'

from app import app, db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_get_data(client):
    res = client.get('/api/data')
    assert res.status_code == 200
    assert res.json == []

def test_add_data(client):
    res = client.post('/api/data', json={"title": "Test Item"})
    assert res.status_code == 201
    assert res.json['title'] == "Test Item"
