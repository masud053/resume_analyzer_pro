import spacy, re
from typing import List, Dict
nlp = spacy.load('en_core_web_sm')

COMMON_SKILLS = [
    'python','machine learning','deep learning','nlp','natural language processing',
    'sql','tensorflow','pytorch','scikit-learn','aws','docker','kubernetes',
    'git','rest api','flask','streamlit','pandas','numpy','matplotlib','etl'
]

def extract_skills(text: str, skills_list: List[str]=None) -> List[str]:
    skills = set()
    t = text.lower()
    list_use = skills_list or COMMON_SKILLS
    for s in list_use:
        if s in t:
            skills.add(s)
    # noun chunks
    doc = nlp(text)
    for chunk in doc.noun_chunks:
        cand = chunk.text.lower().strip()
        if cand in list_use:
            skills.add(cand)
    return sorted(skills)

def parse_experience_years(text: str) -> float:
    # Find "X years" or Year ranges, sum durations (heuristic)
    total = 0.0
    for m in re.finditer(r'(\d+)\s+years?', text.lower()):
        total += float(m.group(1))
    for m in re.finditer(r'(19|20)\d{2}\s*[-–]\s*(19|20)\d{2}', text):
        try:
            years = re.findall(r'(19|20)\d{2}', m.group(0))
            if len(years) >= 2:
                a = int(m.group(0)[:4])
                b = int(m.group(0)[-4:])
                total += abs(b - a)
        except:
            pass
    return total
