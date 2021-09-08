# remade from example code found at
# https://automatetheboringstuff.com/2e/chapter15/
# thank Jesus :)

# import re
import docx


# working if run from utils folder

def get_full_text(filename):
    doc = docx.Document(filename)
    full_text = []
    # parsing plain text paragraphs
    prgrphs = doc.paragraphs
    print('paragraphs found:', len(prgrphs))
    for paragraph in prgrphs:
        full_text.append(paragraph.text)
    # parsing text in tables
    tables = doc.tables
    print('tables found: ', len(tables))
    for table in tables:
        for row in table.rows:
            for cell in row.cells:
                full_text.append(cell.text)

    return '\n'.join(full_text)


# print(get_full_text('../assets/1158.docx'))
