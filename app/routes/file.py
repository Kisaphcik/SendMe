from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
from app import db
from app.models.file import File
from app.utils.storage import save_file
import os

bp = Blueprint('file', __name__)

@bp.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        filepath = save_file(file)
        new_file = File(filename=file.filename, filepath=filepath, user_id=1)  # Hardcoded user_id for simplicity
        db.session.add(new_file)
        db.session.commit()
        flash('File uploaded successfully')
        return redirect(url_for('file.files'))
    return render_template('upload.html')

@bp.route('/files')
def files():
    files = File.query.all()
    return render_template('files.html', files=files)

@bp.route('/download/<int:file_id>')
def download(file_id):
    file = File.query.get_or_404(file_id)
    return send_file(file.filepath, as_attachment=True)