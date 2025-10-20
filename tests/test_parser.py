from resume_parser import clean_text, split_sections
def test_clean_and_split():
    sample = """John Doe\nExperience\n- Data Scientist (2018-2020)\nSkills\nPython, SQL\nEducation\nMSc"""
    c = clean_text(sample)
    secs = split_sections(c)
    assert 'experience' in secs
    assert 'skills' in secs
