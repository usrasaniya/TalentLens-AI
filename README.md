# 🧠 TalentLens AI™

### AI-Powered Resume Screening & Candidate Evaluation Platform

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![Flask](https://img.shields.io/badge/Flask-2.x-black?style=flat-square&logo=flask)
![Google Gemini](https://img.shields.io/badge/Google-Gemini_AI-orange?style=flat-square&logo=google)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-purple?style=flat-square)

---

## 🚀 About

**TalentLens AI™** is an intelligent recruitment assistant that evaluates resumes against job descriptions using **Google Gemini AI** — giving recruiters instant skill match scores, strengths analysis, risk assessment, and structured hiring recommendations.

> Built as part of an AI/ML project under the **SafeCore FY26 ML/AI Program**.

---

## ✨ Features

| Feature | Description |
|---|---|
| 📄 Resume Upload | Supports PDF, DOCX, and TXT formats |
| 🧠 AI Evaluation | Powered by Google Gemini 1.5 Flash |
| 🎯 Match Scoring | 0–100 candidate-to-JD match score |
| 🛡️ Risk Assessment | Flags Low / Moderate / High risk candidates |
| 📊 Analytics Dashboard | Live charts, rankings & cohort stats |
| 💾 CSV Export | Download all evaluations as structured CSV |
| ⚡ Fast Processing | Full scorecard generated in under 15 seconds |
| 🔁 Multi-Candidate | Evaluate and compare unlimited candidates |

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        USER BROWSER                         │
│              (Upload Resume + Job Description)              │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTP Request
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                     FLASK WEB SERVER                        │
│                        (app.py)                             │
│                                                             │
│   Route: /evaluate  ──►  Resume Processing Pipeline         │
│   Route: /dashboard ──►  Analytics & Rankings               │
│   Route: /api/export──►  CSV Download                       │
└──────┬──────────────────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────┐
│           PROCESSING PIPELINE            │
│                                          │
│  1. resume_parser.py                     │
│     └── Extract text from PDF/DOCX/TXT  │
│                                          │
│  2. text_preprocessor.py                 │
│     └── Clean & normalize text           │
│                                          │
│  3. ai_evaluator.py                      │
│     └── Send to Google Gemini API        │
│     └── Receive structured JSON result   │
│                                          │
│  4. report_generator.py                  │
│     └── Save to CSV via Pandas           │
└──────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────┐
│           GOOGLE GEMINI API              │
│   Input:  Resume Text + Job Description  │
│   Output: JSON Scorecard                 │
│   ├── candidate_name                     │
│   ├── match_score (0–100)                │
│   ├── strengths []                       │
│   ├── missing_skills []                  │
│   ├── recommendation                     │
│   ├── risk_assessment                    │
│   └── candidate_summary                  │
└──────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
TalentLens_AI/
│
├── app.py                        # Main Flask application & routes
├── .env                          # Environment variables (API keys)
├── requirements.txt              # Python dependencies
│
├── modules/
│   ├── __init__.py
│   ├── resume_parser.py          # PDF/DOCX/TXT text extraction
│   ├── text_preprocessor.py      # Text cleaning & normalization
│   ├── ai_evaluator.py           # Google Gemini API integration
│   └── report_generator.py       # CSV save/load via Pandas
│
├── templates/
│   ├── base.html                 # Base layout (navbar, fonts, styles)
│   ├── index.html                # Landing page with animations
│   ├── evaluate.html             # Resume upload & scorecard view
│   └── dashboard.html            # Analytics dashboard with Chart.js
│
├── uploads/                      # Temporary resume storage (auto-cleared)
└── output/
    └── candidate_scores.csv      # Persistent evaluation results
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3.10+, Flask 2.x |
| **AI Model** | Google Gemini 1.5 Flash (via `google-genai`) |
| **Resume Parsing** | pdfplumber (PDF), python-docx (DOCX) |
| **Data Processing** | Pandas |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **Charts** | Chart.js |
| **Fonts** | Syne, DM Mono, Inter (Google Fonts) |
| **Environment** | python-dotenv |
| **File Handling** | Werkzeug |

---

## ⚙️ How to Run

### 1. Clone the Repository
```bash
git clone https://github.com/usrasaniya/TalentLens-AI.git
cd TalentLens-AI
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up Your API Key
Create a `.env` file in the root folder:
```
GEMINI_API_KEY=your_google_gemini_api_key_here
```
> Get your free API key at: https://aistudio.google.com/app/apikey

### 4. Run the App
```bash
python app.py
```
The app will automatically open at **http://127.0.0.1:5000**

---

## 🔄 How It Works

```
Step 1 → Recruiter uploads a resume (PDF/DOCX/TXT)
           and pastes the Job Description

Step 2 → resume_parser.py extracts raw text
           from the uploaded file

Step 3 → text_preprocessor.py cleans and
           normalizes both resume and JD text

Step 4 → ai_evaluator.py sends both texts
           to Google Gemini with a structured prompt

Step 5 → Gemini returns a JSON scorecard with:
           match score, recommendation, risk level,
           strengths, and missing skills

Step 6 → Results displayed on screen + saved to CSV

Step 7 → Dashboard aggregates all evaluations
           with ranked candidates, charts & stats
```

---

## 📊 Scorecard Output Example

```json
{
  "candidate_name": "John Doe",
  "match_score": 78,
  "recommendation": "Moderate Fit",
  "risk_assessment": "Low Risk",
  "strengths": ["Python", "SQL", "REST APIs", "Data Analysis"],
  "missing_skills": ["AWS", "Docker", "Kubernetes"],
  "candidate_summary": "Strong backend developer with 3 years experience..."
}
```

---

## 🔮 Future Enhancements

- [ ] 🔐 User authentication & multi-recruiter support
- [ ] 📧 Auto-email shortlisted candidates
- [ ] 🗂️ ATS integration (Workday, Greenhouse, Lever)
- [ ] 📱 Mobile-responsive UI overhaul
- [ ] 🌍 Multi-language resume support
- [ ] 🤖 Batch evaluation (upload multiple resumes at once)
- [ ] 📈 Historical trend analytics per job role
- [ ] 🧪 A/B testing different JD prompt strategies
- [ ] ☁️ Cloud deployment (AWS / Railway / Render)

---

## 📦 Requirements

```
flask
python-dotenv
pdfplumber
python-docx
pandas
google-genai
werkzeug
```

---

## 👩‍💻 Developed By

<table>
  <tr>
    <td align="center">
      <b>Usra Saniya A</b><br/>
      <sub>AI/ML Developer · SafeCore FY26 Program</sub><br/>
      <a href="https://github.com/usrasaniya">GitHub</a>
    </td>
  </tr>
</table>

---

## 📄 License

This project is licensed under the **MIT License** — feel free to use, modify, and distribute.

---

<p align="center">
  <b>TalentLens AI™</b> — Built with 🧠 + ☕ by Usra Saniya A
</p>
