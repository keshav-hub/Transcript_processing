import pdfplumber
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pymongo import MongoClient

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client['transcript_analysis']
collection = db['questions_answers']

def parse_pdf(file_path):
    """Extracts text from a PDF file."""
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

def extract_dialog(text):
    """Extracts dialog lines from the transcript."""
    lines = text.split("\n")
    dialog = []
    for line in lines:
        if "|" in line:
            time, content = line.split("|", 1)
            speaker, message = content.split(" ", 1)
            dialog.append((time.strip(), speaker.strip(), message.strip()))
    return dialog

def extract_questions(dialog):
    """Identifies and extracts questions from the dialog."""
    questions = []
    for time, speaker, message in dialog:
        if "?" in message:
            questions.append((time, speaker, message))
    return questions

def find_similar_questions(questions):
    """Finds similar questions and counts their occurrences."""
    vectorizer = TfidfVectorizer().fit_transform([q[2] for q in questions])
    vectors = vectorizer.toarray()
    cosine_matrix = cosine_similarity(vectors)

    similar_questions = []
    for i in range(len(questions)):
        similar_count = sum(cosine_matrix[i] > 0.8) - 1  # Exclude self-similarity
        if similar_count > 0:
            similar_questions.append((questions[i], similar_count))
    return similar_questions

def store_questions(questions):
    """Stores the top 5 questions in MongoDB."""
    top_5_questions = questions[:5]
    collection.insert_many([{'question': q[0][2], 'answer': '', 'rating': '', 'count': q[1]} for q in top_5_questions])

def rate_answers():
    """Placeholder for rating logic to rate answers in MongoDB."""
    for qa in collection.find():
        answer = qa['answer']
        rating = 'Average'  # Replace with real logic
        collection.update_one({'_id': qa['_id']}, {'$set': {'rating': rating}})

def process_transcripts():
    """Processes all PDF transcripts in the data/ folder."""
    folder_path = 'data'
    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            file_path = os.path.join(folder_path, filename)
            text = parse_pdf(file_path)
            dialog = extract_dialog(text)
            questions = extract_questions(dialog)
            similar_questions = find_similar_questions(questions)
            store_questions(similar_questions)
    rate_answers()
