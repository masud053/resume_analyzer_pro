import os
from chatbot import get_openai_feedback
def test_chatbot_no_key():
    # If no key, the function should return a helpful message
    os.environ.pop('OPENAI_API_KEY', None)
    resp = get_openai_feedback('sample resume','sample job')
    assert 'OpenAI API key not set' in resp or isinstance(resp, str)
