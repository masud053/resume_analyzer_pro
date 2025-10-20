from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer, util
from typing import Dict
from feature_extractor import extract_skills, parse_experience_years
import yaml, os

cfg = yaml.safe_load(open('config.yaml')) if os.path.exists('config.yaml') else {}
EMBED_MODEL = cfg.get('embedding_model', 'all-MiniLM-L6-v2')

embedder = SentenceTransformer(EMBED_MODEL)

def section_similarity(resume_sections: Dict[str,str], job_sections: Dict[str,str]) -> Dict[str,float]:
    vect = TfidfVectorizer(stop_words='english')
    scores = {}
    for key in ['header','experience','skills','education','other']:
        r = resume_sections.get(key,'') or ''
        j = job_sections.get(key,'') or ''
        if r.strip() == '' and j.strip() == '':
            scores[key] = 0.0
            continue
        vectors = vect.fit_transform([r,j])
        sim = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
        # also combine semantic similarity (embeddings)
        try:
            emb_sim = util.cos_sim(embedder.encode(r, convert_to_tensor=True),
                                   embedder.encode(j, convert_to_tensor=True)).item()
        except Exception:
            emb_sim = 0.0
        scores[key] = float(0.6*sim + 0.4*emb_sim)
    return scores

def compute_skill_overlap(resume_text: str, job_text: str, skills_list=None) -> float:
    r = set(extract_skills(resume_text, skills_list))
    j = set(extract_skills(job_text, skills_list))
    if not j:
        return 0.0
    return float(len(r & j) / len(j))

def experience_score(resume_text: str) -> float:
    years = parse_experience_years(resume_text)
    return min(years/10.0, 1.0)

def overall_score(section_scores: Dict[str,float], skill_overlap: float, exp_score: float) -> float:
    weights = cfg.get('scoring', {}).get('weights', {'skills':0.4,'experience':0.3,'education':0.2,'keywords':0.1})
    s = 0.0
    # combine relevant sections
    s += section_scores.get('skills',0.0) * weights.get('skills',0.4)
    s += section_scores.get('experience',0.0) * weights.get('experience',0.3)
    s += section_scores.get('education',0.0) * weights.get('education',0.2)
    # keywords weight applied as skill_overlap
    s += skill_overlap * weights.get('keywords',0.1)
    # blend with experience normalized
    final = min(max(s*0.9 + exp_score*0.1, 0.0), 1.0)
    return float(final)
