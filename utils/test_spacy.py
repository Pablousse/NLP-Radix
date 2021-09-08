import spacy

nlp = spacy.load('en_core_web_sm')
# a new way to add exceptions for a tokenizer
# each pattern should be a list of dicts
# and Matcher.add expecting a list, so => [[{}]]
nlp.get_pipe("attribute_ruler").add([[{"TEXT": "Vegas"}]], {"LEMMA": "Las Vegas"})

doc = nlp(u'You are flying to Paris. I flew to Vegas a year ago.')
for token in doc:
    # mind undescore after .lemma => .lemma_
    print(token.text, '\t', token.lemma_, '\t', token.pos_, '\t', token.dep_, '\t', token.ent_type_)  # token.head.text, '\t',
    # if token.ent_type != 0:
    #     print(token.text, token.ent_type_)
# print([w.text for w in doc if w.tag_ == 'VBG' or w.tag_ == 'VB'])
# print([w.text for w in doc if w.pos_ == 'PROPN'])

# for sent in doc.sents:
#     print([w.text for w in sent if w.dep_ == 'ROOT' or w.dep_ == 'pobj'])
