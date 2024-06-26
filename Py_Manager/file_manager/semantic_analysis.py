import spacy

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

def analyze_text(text):
    doc = nlp(text)
    summary = {
        "entities": [(ent.text, ent.label_) for ent in doc.ents],
        "noun_chunks": [chunk.text for chunk in doc.noun_chunks],
        "keywords": [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    }
    return summary

def analyze_file_contents(file_path):
    with open(file_path, "r") as file:
        text = file.read()
    return analyze_text(text)

def analyze_file_name(file_name):
    return analyze_text(file_name)
