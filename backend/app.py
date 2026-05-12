import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Настройка базы данных
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://user:pass@localhost:5432/db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)

@app.route('/api/data', methods=['GET'])
def get_data():
    items = Item.query.all()
    return jsonify([{"id": i.id, "title": i.title} for i in items])

@app.route('/api/data', methods=['POST'])
def add_data():
    data = request.json
    if not data or 'title' not in data:
        return jsonify({"error": "No title"}), 400
    new_item = Item(title=data['title'])
    db.session.add(new_item)
    db.session.commit()
    return jsonify({"id": new_item.id, "title": new_item.title}), 201

@app.route('/api/data/<int:item_id>', methods=['DELETE'])
def delete_data(item_id):
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return '', 204

# ВАЖНО: Весь исполняемый код переносим сюда
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
