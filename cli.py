import argparse
from resume_parser import extract_text, clean_text, split_sections
from analyzer import section_similarity, compute_skill_overlap, experience_score, overall_score
from feature_extractor import extract_skills, parse_experience_years

def run(resume, job):
    r = extract_text(resume)
    j = open(job, 'r', encoding='utf-8').read()
    r_c = clean_text(r); j_c = clean_text(j)
    r_sec = split_sections(r_c); j_sec = split_sections(j_c)
    sec_scores = section_similarity(r_sec, j_sec)
    skill_overlap = compute_skill_overlap(r_c, j_c)
    exp = experience_score(r_c)
    total = overall_score(sec_scores, skill_overlap, exp)
    print(f'Overall Match Score: {total*100:.2f}%')
    print('Section scores:'); print(sec_scores)
    print(f'Skill overlap: {skill_overlap*100:.1f}%'); print(f'Experience (years approx): {parse_experience_years(r_c)}')
    print('Top skills:', extract_skills(r_c))

if __name__=='__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--resume', required=True)
    p.add_argument('--job', required=True)
    args = p.parse_args()
    run(args.resume, args.job)
