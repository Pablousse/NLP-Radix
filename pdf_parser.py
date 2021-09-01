import fitz
from bs4 import BeautifulSoup

doc = fitz.open("assets/pdf/7.pdf")
page1 = doc[0]
words = page1.get_text("words")

blocks = []
block_line = []

for line in page1.get_text("html").splitlines():
    soup_line = BeautifulSoup(line, "lxml")
    spans = soup_line.find_all("span")
    if spans:
        b_tag = soup_line.find('b')
        if b_tag:
            blocks.append(block_line)
            block_line = []

        for span in spans:
            block_line.append(span.text)


blocks.append(block_line)


for block in blocks:
    print(block)

# print(page1.get_text("html"))
