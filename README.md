# AI Resume Analyzer Pro

**AI Resume Analyzer Pro** — production-ready Python project to extract, analyze, score, and improve resumes against job descriptions.
This version includes advanced NLP (semantic embeddings), OpenAI GPT feedback enabled-by-default (via `OPENAI_API_KEY`), Streamlit UI, CLI, PDF reporting, tests, Docker, and CI.

## Highlights
- Semantic matching using `sentence-transformers`
- Section-aware TF-IDF + semantic scoring
- Skill extraction, NER, experience parsing
- OpenAI GPT feedback (enabled when `OPENAI_API_KEY` is set)
- Streamlit frontend + CLI runner
- PDF report generation
- Dockerfile + GitHub Actions CI
- Unit tests with `pytest`

## Quickstart (short)
1. Copy `.env.example` to `.env` and set `OPENAI_API_KEY` if you want GPT feedback.
2. Create venv and install:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```
3. Run Streamlit UI:
```bash
streamlit run app.py
```

## Example CLI usage
```bash
python cli.py --resume sample_data/resume1.pdf --job sample_data/job_description.txt
```

## Project structure
See repository files (app.py, analyzer.py, resume_parser.py, feature_extractor.py, chatbot.py, report_generator.py, tests/, sample_data/, Dockerfile, .github/workflows/ci.yml).
