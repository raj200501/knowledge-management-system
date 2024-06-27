from flask import request, jsonify
from models import KnowledgeEntry, db

def init_routes(app):
    @app.route('/entries', methods=['GET'])
    def get_entries():
        entries = KnowledgeEntry.query.all()
        return jsonify([entry.to_dict() for entry in entries])

    @app.route('/entry', methods=['POST'])
    def add_entry():
        data = request.get_json()
        new_entry = KnowledgeEntry(title=data['title'], content=data['content'])
        db.session.add(new_entry)
        db.session.commit()
        return jsonify(new_entry.to_dict())

    @app.route('/entry/<int:id>', methods=['GET'])
    def get_entry(id):
        entry = KnowledgeEntry.query.get(id)
        if entry:
            return jsonify(entry.to_dict())
        return jsonify({'error': 'Entry not found'}), 404

    @app.route('/entry/<int:id>', methods=['PUT'])
    def update_entry(id):
        data = request.get_json()
        entry = KnowledgeEntry.query.get(id)
        if entry:
            entry.title = data['title']
            entry.content = data['content']
            db.session.commit()
            return jsonify(entry.to_dict())
        return jsonify({'error': 'Entry not found'}), 404

    @app.route('/entry/<int:id>', methods=['DELETE'])
    def delete_entry(id):
        entry = KnowledgeEntry.query.get(id)
        if entry:
            db.session.delete(entry)
            db.session.commit()
            return jsonify({'message': 'Entry deleted'})
        return jsonify({'error': 'Entry not found'}), 404
