from flask import Flask, jsonify, request
from parser import process_transcripts, collection
from bson.objectid import ObjectId

app = Flask(__name__)

@app.route('/questions', methods=['GET'])
def get_questions():
    """Retrieve all stored questions and answers."""
    questions = list(collection.find({}, {'_id': 0}))
    return jsonify(questions)

@app.route('/question', methods=['POST'])
def add_question():
    """Add a new question and answer."""
    question = request.json
    collection.insert_one(question)
    return jsonify({'msg': 'Question added successfully'})

@app.route('/question/<id>', methods=['PUT'])
def update_question(id):
    """Update a question and answer by ID."""
    data = request.json
    collection.update_one({'_id': ObjectId(id)}, {'$set': data})
    return jsonify({'msg': 'Question updated successfully'})

@app.route('/question/<id>', methods=['DELETE'])
def delete_question(id):
    """Delete a question and answer by ID."""
    collection.delete_one({'_id': ObjectId(id)})
    return jsonify({'msg': 'Question deleted successfully'})

@app.route('/process_transcripts', methods=['POST'])
def trigger_processing():
    """Trigger processing of transcripts in the data/ folder."""
    process_transcripts()
    return jsonify({'msg': 'Transcripts processed successfully'})

if __name__ == '__main__':
    app.run(debug=True)
