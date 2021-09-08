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
# extended regex to match contry codes inside brackets, works slower and may return a number with ) inside
# {'REGEX': '^\s*[-. (]*?(?:\+?(\d{1,3}))?[-. )]*?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*$'}
tel_pattern = [{'TEXT': {'REGEX': '^\s*[-. (]*?(?:\+?(\d{1,3}))?[-. )]*?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*$'}}]
simple_email_regex = '[\w%-_.+]+@[\w%-_.+]+\.\w+'

# email_pattern = [{"TEXT": {"REGEX": "(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|'(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*')@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"}}]
email_pattern = [{"TEXT": {"REGEX": simple_email_regex}}]

# emails_list = []
for i in range(1, 10):
    print(f'reading docX #{i}')
    text = read_docX.get_full_text(f'../assets/{i}.docx')
    print(find_matches(text, name_pattern, 'name'))
    print(find_matches(text, tel_pattern, 'tel'))
    print(find_matches(text, email_pattern, 'email'))

    # emails = find_matches(text, email_pattern, 'email')
    # emails_list.append(emails)
# print(len(emails_list), emails_list)
# for simple or extended email regex this gives same results:
# 9 [[], [], [satyamce@gmail.com], [e-Mail:salman.ali19@gmail.com, ali_salman_143@yahoo.com], [], [Email:alamdar1710@gmail.com], [], [rmoumita03@gmail.com], []]

# PROBLEM is my scraper did not grab email addresses witch are links in docX files. sad :( ...

"""
We would like to extract information about:

education
previous job title
skills
personal information (address, mail, name, phone number)
hobby’s
"""