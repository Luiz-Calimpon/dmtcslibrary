import os
from werkzeug.utils import secure_filename
from sentence_transformers import SentenceTransformer
import numpy as np
from app.models import Case
from app import db
from flask import current_app

model = SentenceTransformer('all-MiniLM-L6-v2')

ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_file(file, filename):
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    return file_path

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        return file.read()

def search_cases(query, cases=None):
    if cases is None:
        cases = Case.query.all()

    query_embedding = model.encode(query)
    results = []

    for case in cases:
        if case.embedding is None:
            case.embedding = model.encode(case.content)
        
        similarity = np.dot(query_embedding, case.embedding) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(case.embedding)
        )
        result = case.to_dict()
        result['score'] = float(similarity)
        results.append(result)

    results.sort(key=lambda x: x['score'], reverse=True)
    return results[:5]  # Return top 5 results

def retrain_model(app):
    with app.app_context():
        print("Retraining model...")
        cases = Case.query.all()
        texts = [case.content for case in cases]
        model.fit(texts)
        
        # Update embeddings for all cases
        for case in cases:
            case.embedding = model.encode(case.content)
        db.session.commit()
        
        print("Model retraining complete.")