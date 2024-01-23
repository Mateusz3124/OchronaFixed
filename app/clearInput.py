import re

def clearInput(text):
    pattern = re.compile(r'^[., a-zA-Z0-9!@$%^&*\[\]]+$')
    if text is None:
        return ""
    if len(text) > 60:
        return ""
    match = pattern.match(text)
    if bool(match):
        return text
    else:
        return ""