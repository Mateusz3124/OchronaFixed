import re

def clearInput(text):
    pattern = re.compile(r'^[., a-zA-Z0-9]+$')
    if text is None:
        return ""
    text = str(text)
    if len(text) > 75:
        return ""
    match = pattern.match(text)
    if bool(match):
        return text
    else:
        return ""
    
def clearInputPassword(text):
    pattern = re.compile(r'^[., a-zA-Z0-9!@#$%^&*()\[\]]+$')
    if text is None:
        return ""
    if len(text) > 30:
        return ""
    match = pattern.match(text)
    if bool(match):
        return text
    else:
        return ""