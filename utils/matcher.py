import spacy
from spacy.matcher import Matcher

nlp = spacy.load('en_core_web_sm')
matcher = Matcher(nlp.vocab)


def find_matches(text: str, pattern: list, pattern_name: str) -> list:
    """
    generic function to find matching patterns in a given sample of text.
    """
    doc = nlp(text)
    matcher.add(pattern_name, [pattern])
    matches = matcher(doc)
    matcher.remove(pattern_name)
    spans_found = [doc[start:end] for match_id, start, end in matches]
    return spacy.util.filter_spans(spans_found)
