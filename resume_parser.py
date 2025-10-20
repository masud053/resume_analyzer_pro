import pdfplumber, docx, re
from typing import Dict

def extract_text_from_pdf(path: str) -> str:
    text = ''
    with pdfplumber.open(path) as pdf:
        for p in pdf.pages:
            page_text = p.extract_text()
            if page_text:
                text += page_text + '\n'
    return text

def extract_text_from_docx(path: str) -> str:
    doc = docx.Document(path)
    return '\n'.join(p.text for p in doc.paragraphs)

def extract_text(path: str) -> str:
    path = str(path)
    if path.lower().endswith('.pdf'):
        return extract_text_from_pdf(path)
    if path.lower().endswith('.docx'):
        return extract_text_from_docx(path)
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()

def clean_text(text: str) -> str:
    t = re.sub(r'\s+', ' ', text)
    return t.strip()

def split_sections(text: str) -> Dict[str,str]:
    sections = {'header':'', 'experience':'', 'education':'', 'skills':'', 'other': ''}
    lower = text.lower()
    markers = {'experience': ['experience','work experience','employment'],
               'education': ['education','academic','degree'],
               'skills': ['skills','technical skills','technical competencies']}
    # find indices
    indices = {}
    for key, keys in markers.items():
        for k in keys:
            idx = lower.find(k)
            if idx != -1:
                indices[key] = idx
                break
    # sort and slice
    sorted_items = sorted(indices.items(), key=lambda x: x[1])
    last = 0
    for i, (sec, idx) in enumerate(sorted_items):
        start = idx
        end = sorted_items[i+1][1] if i+1 < len(sorted_items) else len(text)
        sections[sec] = text[start:end].strip()
    if not any(sections.values()):
        sections['other'] = text
    # header heuristic
    if 'experience' in indices:
        sections['header'] = text[:indices['experience']].strip()
    return sections
