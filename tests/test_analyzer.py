from analyzer import compute_skill_overlap, experience_score
def test_skill_overlap_and_experience():
    r = 'Python, SQL, AWS, Docker'
    j = 'Python, Docker, Kubernetes'
    assert compute_skill_overlap(r,j) >= 0.0
    # experience parser should handle "2 years"
    assert experience_score('Worked 3 years on projects') >= 0.0
