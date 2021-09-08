import spacy
from spacy.matcher import Matcher

import read_docX

nlp = spacy.load('en_core_web_sm')
matcher = Matcher(nlp.vocab)


def find_matches(text: str, pattern: list, pattern_name: str) -> list:
    """generic function to find matching patterns in a given sample of text."""

    doc = nlp(text)
    matcher.add(pattern_name, [pattern])
    matches = matcher(doc)
    matcher.remove(pattern_name)
    spans_found = [doc[start:end] for match_id, start, end in matches]
    return spacy.util.filter_spans(spans_found)


# "LENGTH": {">": 2}
name_pattern = [{'POS': 'PROPN', 'ENT_TYPE': 'PERSON', 'TEXT': {'REGEX': '^[^.]+$'}}, {'POS': 'PROPN', 'ENT_TYPE': 'PERSON', 'TEXT': {'REGEX': '^[^.]+$'}, 'OP': '+'}]
# extended regex to match contry codes inside brackets, works slower
# {'REGEX': '^\s*[-. (]*?(?:\+?(\d{1,3}))?[-. )]*?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*$'}
tel_pattern = [{'TEXT': {'REGEX': '^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*$'}}]

for i in range(1, 50):
    print(f'reading docX #{i}')
    text = read_docX.get_full_text(f'../assets/{i}.docx')
    print(find_matches(text, name_pattern, 'name'))
    print(find_matches(text, tel_pattern, 'tel'))
