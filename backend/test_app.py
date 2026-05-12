import pytest
from app import app, db, Item

@pytest.fixture
def client():
    # 1. Форсированно меняем настройки на SQLite в памяти
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True
    
    # 2. Создаем контекст и таблицы в этой временной базе
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client # Здесь запускаются сами тесты
        
        # 3. После тестов всё очищаем
        with app.app_context():
            db.drop_all()

def test_get_data_empty(client):
    res = client.get('/api/data')
    assert res.status_code == 200
    assert res.json == []

def test_add_and_get_data(client):
    # Тест POST
    post_res = client.post('/api/data', json={"title": "Test Task"})
    assert post_res.status_code == 201
    
    # Тест GET после добавления
    get_res = client.get('/api/data')
    assert len(get_res.json) == 1
    assert get_res.json[0]['title'] == "Test Task"

def test_delete_data(client):
    # Сначала добавим
    item = client.post('/api/data', json={"title": "To Delete"}).json
    # Затем удалим
    del_res = client.delete(f'/api/data/{item["id"]}')
    assert del_res.status_code == 204
