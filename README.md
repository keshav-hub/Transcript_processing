## Features

1. Parse PDF transcripts to extract dialogues.
2. Identify and count similar questions asked by the seller using vector-based similarity.
3. Store top 5 questions and their corresponding answers in MongoDB.
4. Rate answers as Best, Good, or Average.
5. Provide CRUD APIs 

## Setup

### Installation
1. Python 3.9
2. MongoDB
3. Start MongoDB:

    ```bash
    brew services start mongodb/brew/mongodb-community@6.0
    ```

### Running the Application

1. **Run the Flask application**:

   
    python app.py

2. **Trigger the transcript processing via the API**:

    ```bash
    curl -X POST http://127.0.0.1:5000/process_transcripts
    ```

### API Endpoints

- **GET /questions**: Retrieve all stored questions and answers.
- **POST /question**: Add a new question and answer.
- **PUT /question/<id>**: Update a question and answer by ID.
- **DELETE /question/<id>**: Delete a question and answer by ID.
- **POST /process_transcripts**: Trigger processing of transcripts in the `data/` folder.

## Libraries Used

- `flask` for creating the REST APIs.
- `pymongo` for MongoDB interactions.
- `pdfplumber` for PDF parsing.
- `scikit-learn` for text processing and similarity calculations.

