# remade from example code found at
# https://automatetheboringstuff.com/2e/chapter15/
# thank Jesus :)

# import re
import docx


# working if run from utils folder
def get_full_text(filename):
    doc = docx.Document(filename)
    prgrphs = doc.paragraphs
    print('paragraphs found:', len(prgrphs))
    full_text = []
    for paragraph in prgrphs:
        full_text.append(paragraph.text)
    return '\n'.join(full_text)


print(get_full_text('../assets/1.docx'))
