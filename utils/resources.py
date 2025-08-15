LEARNING_LINKS = {
    "python": ["https://docs.python.org/3/tutorial/","https://www.freecodecamp.org/learn/"],
    "flask": ["https://flask.palletsprojects.com/","https://www.freecodecamp.org/learn/"],
    "machine learning": ["https://scikit-learn.org/stable/tutorial/","https://www.coursera.org/learn/machine-learning"]
}

def learning_resources(missing_skills):
    out = {}
    for s in missing_skills:
        key = s.lower()
        out[s] = LEARNING_LINKS.get(key, [f"https://www.google.com/search?q=learn+{key.replace(' ','+')}" ])
    return out