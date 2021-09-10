from matcher import find_matches

def find_personal_info(text: 'str') -> list:
    """
    function returns 3 lists with personal information
    find in a sample of provided text,
    based on a few build-in patterns for Matcher module in Spacy library
    """
    # name pattern consist 2 or more consecutive pronouns that do not have any dots within
    # works good with small chunk of text taken from the start of a resume
    name_pattern = [{'POS': 'PROPN', 'TEXT': {'REGEX': '^[^.]+$'}},
                    {'POS': 'PROPN', 'TEXT': {'REGEX': '^[^.]+$'}, 'OP': '+'}]
    # similar to name pattern but pronouns also should be recognized by Spacy as  named entities
    # could be applied to a large text but could miss rare names or give false results for some capitalized words
    named_entity_pattern = [{'POS': 'PROPN', 'ENT_TYPE': 'PERSON', 'TEXT': {'REGEX': '^[^.]+$'}},
                            {'POS': 'PROPN', 'ENT_TYPE': 'PERSON', 'TEXT': {'REGEX': '^[^.]+$'}, 'OP': '+'}]
    # 11 digit number
    tel_regex = '^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*$'
    # extended regex to match contry codes inside brackets, works slower and may return a number with ) inside
    tel_ext_regex = '^\s*[-. (]*?(?:\+?(\d{1,3}))?[-. )]*?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*$'
    tel_pattern = [{'TEXT': {'REGEX': tel_ext_regex}}]

    simple_email_regex = '[\w%-_.+]+@[\w%-_.+]+\.\w+'
    email_pattern = [{"TEXT": {"REGEX": simple_email_regex}}]
    # patterns = {'name': name_pattern, 'telephone': tel_pattern, 'email': email_pattern}
    name_list = find_matches(text, name_pattern, 'name')
    tel_list = find_matches(text, tel_pattern, 'name')
    email_list = find_matches(text, email_pattern, 'name')
    return name_list, tel_list, email_list
