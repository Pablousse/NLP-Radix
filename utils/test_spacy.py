import spacy

nlp = spacy.load('en_core_web_sm')
# a new way to add exceptions for a tokenizer
# each pattern should be a list of dicts
# and Matcher.add expecting a list, so => [[{}]]
nlp.get_pipe("attribute_ruler").add([[{"TEXT": "Lon"}]], {"LEMMA": "London"})

doc = nlp(u'You are flying to Lon')
for token in doc:
    # mind undescore after .lemma => .lemma_
    print(token.text, token.lemma_)
