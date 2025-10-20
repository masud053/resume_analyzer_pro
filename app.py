import streamlit as st
from resume_parser import extract_text, clean_text, split_sections
from analyzer import section_similarity, compute_skill_overlap, experience_score, overall_score, embedder
from feature_extractor import extract_skills, parse_experience_years
from chatbot import get_openai_feedback
from report_generator import generate_report
import tempfile, os, yaml

st.set_page_config(page_title='AI Resume Analyzer Pro', layout='wide')
st.title('AI Resume Analyzer Pro')

st.sidebar.header('Options')
use_gpt = st.sidebar.checkbox('Enable GPT feedback (requires OPENAI_API_KEY)', value=True)
show_sections = st.sidebar.checkbox('Show section previews', value=True)

job_text = st.text_area('Paste Job Description', height=200)
uploaded = st.file_uploader('Upload Resume (PDF/DOCX/TXT)', type=['pdf','docx','txt'])

if uploaded and job_text:
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded.name)[1]) as tmp:
        tmp.write(uploaded.getvalue())
        tmp_path = tmp.name
    raw = extract_text(tmp_path)
    clean = clean_text(raw)
    job_clean = clean_text(job_text)
    r_sec = split_sections(clean)
    j_sec = split_sections(job_clean)

    st.header('Analysis')
    sec_scores = section_similarity(r_sec, j_sec)
    skill_overlap = compute_skill_overlap(clean, job_clean)
    exp_scr = experience_score(clean)
    total = overall_score(sec_scores, skill_overlap, exp_scr)

    st.metric('Overall Match Score', f"{total*100:.2f}%")
    st.subheader('Section scores')
    st.json(sec_scores)
    st.subheader('Skill overlap')
    st.write(f"{skill_overlap*100:.1f}%")
    st.subheader('Experience (years heuristic)')
    st.write(f"{parse_experience_years(clean)} years approx.")

    if show_sections:
        st.subheader('Sections preview')
        for k,v in r_sec.items():
            st.markdown(f"**{k.title()}**\n{v[:800]}..." if v else f"**{k.title()}** - (empty)")

    st.subheader('Top extracted skills')
    st.write(extract_skills(clean)[:60])

    if use_gpt:
        with st.spinner('Getting GPT feedback...'):
            feedback = get_openai_feedback(clean, job_clean)
            st.markdown('### GPT Feedback')
            st.write(feedback)

    # generate report
    if st.button('Generate PDF Report'):
        analysis = {'overall_score': total, 'section_scores': sec_scores, 'suggestions': []}
        tmp_report = os.path.join(tempfile.gettempdir(), 'resume_report.pdf')
        generate_report(tmp_report, analysis, clean)
        with open(tmp_report,'rb') as f:
            st.download_button('Download Report', data=f, file_name='resume_report.pdf', mime='application/pdf')
else:
    st.info('Upload resume and paste job description to run analysis.')
