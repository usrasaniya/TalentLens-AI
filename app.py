import os
import io
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, jsonify, send_file, flash
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

from modules.resume_parser import parse_resume
from modules.text_preprocessor import preprocess_text
from modules.ai_evaluator import evaluate_candidate
from modules.report_generator import save_evaluation, load_all_evaluations

load_dotenv()

app = Flask(__name__)
app.secret_key = "talentlens_ai_secret_key"

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
OUTPUT_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/evaluate', methods=['GET', 'POST'])
def evaluate():
    if request.method == 'GET':
        return render_template('evaluate.html')
    if request.method == 'POST':
        if 'resume' not in request.files:
            flash("No resume file uploaded.", "error")
            return redirect(request.url)
        file = request.files['resume']
        job_description = request.form.get('job_description', '')
        if file.filename == '':
            flash("No file selected.", "error")
            return redirect(request.url)
        if not job_description.strip():
            flash("Job description is required.", "error")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            try:
                raw_text = parse_resume(filepath)
                if not raw_text.strip():
                    flash("Could not extract text from the uploaded resume.", "error")
                    return redirect(request.url)
                cleaned_resume_text = preprocess_text(raw_text)
                cleaned_jd_text = preprocess_text(job_description)
                evaluation_result = evaluate_candidate(cleaned_resume_text, cleaned_jd_text)
                if not evaluation_result:
                    flash("AI Evaluation failed or returned empty results.", "error")
                    return redirect(request.url)
                save_evaluation(evaluation_result, OUTPUT_FOLDER)
                return render_template('evaluate.html', result=evaluation_result, job_description=job_description)
            except Exception as e:
                flash(f"An error occurred: {str(e)}", "error")
                return redirect(request.url)
            finally:
                if os.path.exists(filepath):
                    os.remove(filepath)
        else:
            flash("Allowed file types are txt, pdf, docx.", "error")
            return redirect(request.url)

@app.route('/dashboard')
def dashboard():
    candidates = load_all_evaluations(OUTPUT_FOLDER)
    def get_score(c):
        score = c.get('match_score', 0)
        try:
            return int(score) if score and str(score).strip() else 0
        except ValueError:
            return 0
    candidates.sort(key=get_score, reverse=True)
    total_candidates = len(candidates)
    if total_candidates > 0:
        avg_score = round(sum(get_score(c) for c in candidates) / total_candidates)
        top_candidate = candidates[0].get('candidate_name', 'N/A')
        strong_fits = sum(1 for c in candidates if 'Strong' in c.get('recommendation', ''))
        low_risk = sum(1 for c in candidates if 'Low' in (c.get('risk_assessment') or ''))
        med_risk = sum(1 for c in candidates if 'Moderate' in (c.get('risk_assessment') or ''))
        hi_risk = sum(1 for c in candidates if 'High' in (c.get('risk_assessment') or ''))
    else:
        avg_score = 0
        top_candidate = 'N/A'
        strong_fits = 0
        low_risk = 0
        med_risk = 0
        hi_risk = 0
    stats = {
        'total': total_candidates,
        'avg_score': avg_score,
        'top_candidate': top_candidate,
        'strong_fits': strong_fits,
        'low_risk': low_risk,
        'med_risk': med_risk,
        'hi_risk': hi_risk
    }
    return render_template('dashboard.html', candidates=candidates, stats=stats)

@app.route('/api/export')
def export_csv():
    csv_path = os.path.join(OUTPUT_FOLDER, 'candidate_scores.csv')
    if os.path.exists(csv_path):
        return send_file(csv_path, as_attachment=True, download_name='candidate_scores.csv')
    else:
        flash("No evaluations to export yet.", "error")
        return redirect(url_for('dashboard'))

if __name__ == '__main__':
    import webbrowser, threading
    threading.Timer(1.2, lambda: webbrowser.open('http://127.0.0.1:5000')).start()
    app.run(debug=False)