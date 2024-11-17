from flask import render_template, request, jsonify, current_app
from app import db
from app.models import Case
from app.utils import allowed_file, save_file, read_file, search_cases, retrain_model
from werkzeug.utils import secure_filename
import os

from flask import current_app as app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_cases')
def get_cases():
    cases = Case.query.all()
    return jsonify([case.to_dict() for case in cases])

@app.route('/search')
def search():
    query = request.args.get('query', '')
    results = search_cases(query)
    return jsonify(results)

@app.route('/update_case/<int:id>', methods=['POST'])
def update_case(id):
    data = request.json
    case = Case.query.get_or_404(id)
    case.title = data['title']
    case.type = data['type']
    case.case_no = data['caseNo']
    case.location = data['location']
    db.session.commit()
    retrain_model(current_app._get_current_object())
    return jsonify({'success': True})

@app.route('/delete_case/<int:id>', methods=['POST'])
def delete_case(id):
    case = Case.query.get_or_404(id)
    if case.file_path:
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], case.file_path)
        if os.path.exists(file_path):
            os.remove(file_path)
    db.session.delete(case)
    db.session.commit()
    retrain_model(current_app._get_current_object())
    return jsonify({'success': True})

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = save_file(file, filename)
        content = read_file(file_path)
        file_type = os.path.splitext(filename)[1]

        new_case = Case(
            title=filename,
            type='Unknown',
            case_no='Unknown',
            location='Unknown',
            content=content,
            file_type=file_type,
            file_path=filename
        )
        db.session.add(new_case)
        db.session.commit()

        retrain_model(current_app._get_current_object())

        return jsonify({'success': True, 'filename': filename})
    return jsonify({'success': False, 'error': 'File type not allowed'}), 400

@app.route('/view_case/<int:id>')
def view_case(id):
    query = request.args.get('query', '')
    case = Case.query.get_or_404(id)
    case_dict = case.to_dict()
    case_dict.update({
        'content': case.content,
        'fileType': case.file_type
    })

    if query:
        relevance = search_cases(query, [case])[0]['score']
        case_dict['relevance'] = relevance
    else:
        case_dict['relevance'] = None

    return render_template('view_case.html', case=case_dict)