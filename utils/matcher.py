import spacy
from spacy.matcher import Matcher
import read_docX

_1 = read_docX.get_full_text('../assets/1.docx')
# print(_1)
nlp = spacy.load('en_core_web_sm')
doc = nlp(_1)

matcher = Matcher(nlp.vocab)
# "LENGTH": {">": 2}
# {'POS': 'PROPN', 'ENT_TYPE': 'PERSON', 'TEXT': {'REGEX': '^[^.]+$'}},
name_pattern = [{'POS': 'PROPN', 'ENT_TYPE': 'PERSON', 'TEXT': {'REGEX': '^[^.]+$'}}, {'POS': 'PROPN', 'ENT_TYPE': 'PERSON', 'OP': '+'}]
matcher.add('NAME', [name_pattern])
matches = matcher(doc)
print([doc[start:end] for match_id, start, end in matches])



# meaningful_text = [sent.text for sent in doc.sents if sent.text != '\n']
# print(meaningful_text)

# _person = []
# _tokens = [token.text for token in doc] # if token.text != '\n\n\n\n\n\n\n\n\n'
# print(_tokens)
"""
for token in doc:
    if token.ent_type_ == 'PERSON' and token


for sent in doc.sents:
    for token in sent:
        if token.ent_type_ == 'PERSON':
            if to
            print(token.ent_type_, token.text) # , sent.text
    # print(token.text, '\t', token.lemma_, '\t', token.pos_, '\t', token.dep_, '\t', token.ent_type_)  # token.head.text, '\t',
    # if token.ent_type != 0: # 


"""