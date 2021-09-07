import collections
import fitz
import pandas as pd
# import spacy


def extract_info_from_page(page_number, min_paragraph_size_adjusted, doc):

    page = doc[page_number]
    df_block = pd.DataFrame(page.get_text("blocks"), columns=["x0", "y0", "x1", "y1", "text", "block_number", "block"])
    df_block["text"] = df_block["text"].replace(r'\n', ' ', regex=True)
    df_block["text"] = df_block["text"].str.strip()

    x = page.get_text("dict")

    # print(df_block)

    font_info = []

    for block in x["blocks"]:
        # print(block)
        # text = ""
        size = ""
        font = ""
        color = ""
        number = block["number"]
        is_line_bold = 0
        if 'lines' in block.keys():
            for lines in block["lines"]:
                # print(lines)
                for span in lines["spans"]:
                    # text += span["text"]
                    if span["text"].strip() != "":
                        size += str(span["size"]) if size == "" else "," + str(span["size"])
                        font += str(span["font"]) if font == "" else "," + str(span["font"])
                        color += str(span["color"]) if color == "" else "," + str(span["color"])
            if all( "bold" in i.lower() for i in font.split(",") ):
                is_line_bold = 1
        font_info.append([number, size, font, color, is_line_bold])

    df_info = pd.DataFrame(font_info, columns=["block_number", "size", "font", "color", "is_line_bold"])
    df_block = df_block.merge(df_info, on="block_number")
    df_block["is_title"] = 0
    df_block.loc[(df_block['text'].str.split().str.len() < 4) & (df_block["is_line_bold"] == 1), 'is_title'] = 1
    x = df_block[df_block.index == 5]["font"]
    pd.set_option('display.max_columns', None)
    # print(df_block)


    # Remove empty cells

    df_block = df_block[df_block["text"].replace(" ", "") != ""]

    #

    df_block["next_y0"] = df_block["y0"].shift(-1)
    df_block["next_x0"] = df_block["x0"].shift(-1)
    df_block["previous_x0"] = df_block["x0"].shift(+1)
    df_block["diff"] = df_block["next_y0"] - df_block["y1"]

    new_list_block = []
    text = ""
    x0 = ""

    # print(min_paragraph_size_adjusted)

    for index, row in df_block.iterrows():
        if row["diff"] > min_paragraph_size_adjusted or row["diff"] < 0:
            row["text"] = text + " " + row["text"]
            row["x0"] = x0 if x0 != "" else row["x0"]
            new_list_block.append(row)
            text = ""
            x0 = ""
        else:
            text += row["text"]
            if x0 == "":
                x0 = row["x0"]

    new_df_block = pd.DataFrame(new_list_block)

    new_df_block["next_x0"] = new_df_block["x0"].shift(-1)
    new_df_block["previous_x0"] = new_df_block["x0"].shift(+1)

    return pd.DataFrame(new_df_block)


def extract_info_from_pdf(pdf_path, percentage_adjustment):
    doc = fitz.open(pdf_path)
    page1 = doc[0]

    df_words = pd.DataFrame(page1.get_text("words"), columns=["x0", "y0", "x1", "y1", "text", "block_no", "line_no", "word_no"])

    # Calcul the paragraph size

    df_words["diff"] = df_words["y0"].diff()

    df_words["next_y0"] = df_words["y0"].shift(-1)
    df_words["diff"] = df_words["next_y0"] - df_words["y1"]
    min_paragraph_size = df_words[df_words["diff"] > 0]["diff"].min()
    min_paragraph_size_adjusted = min_paragraph_size + (min_paragraph_size*percentage_adjustment)
    #

    for i in range(0, len(doc)):
        if i == 0:
            df_informations = extract_info_from_page(i, min_paragraph_size_adjusted, doc)
        else:
            df_informations = pd.concat([df_informations, extract_info_from_page(i, min_paragraph_size_adjusted, doc)])

    # print("info")
    # print(df_informations)

    # text = ""
    # new_df_block = []
    # flag = False
    # for index, row in df_informations.iterrows():
    #     if (row["x0"] == row["next_x0"] and row["x0"] != row["previous_x0"]) or (flag == True and row["x0"] == row["next_x0"] and row["x0"] == row["previous_x0"]):
    #         text += row["text"]
    #         flag = True
    #     else:
    #         row["text"] = text + " " + row["text"]
    #         new_df_block.append(row)
    #         text = ""
    #         flag = False

    # df_informations_adjusted = pd.DataFrame(new_df_block)

    df_informations = df_informations.reset_index(drop=True)

    # df_informations_adjusted = df_informations_adjusted.reset_index(drop=True)

    return df_informations


df = extract_info_from_pdf("assets/pdf/12.pdf", 0.2)
# print(df)
# print(df.iloc[7]["text"])

objective = ["objective", "objectives", "synopsis"]
skills = ["skill", "computer", "certification", "technical"]
education = ["educational", "qualification", "academic", "scholastic"]
experience = ["experience", "project", "employment", "internship"]
hobbies = ["hobbies", "curricular", "co-curricular", "activity", "activities"]
personnal = ["personnal", "personality", "personal", "about me"]
other = ["strength", "strenth", "strenght", "declaration", "declairation", "language", "achievements"]
category_list = [objective, skills, education, experience, hobbies, personnal, other]
df["category"] = ""
# print(df)
for categories in category_list:
    for category in categories:
        print(category)
        df.at[df[((df['text'].str.contains(category, case=False)) | (df['text'].str.contains((category+"s"), case=False))) & (df['is_line_bold'] == 1)].index, "category"] = category

print(df)

# nlp = spacy.load('en_core_web_sm')

# doc = nlp("Educational")

# for token in doc:
#     print(token, token.lemma, token.lemma_)

# blocks = []
# block_line = []

# df_html = pd.DataFrame(page1.get_text("html").splitlines())

# print(df_informations2)

# result = pd.concat([df_informations, df_informations2])
# print(result)

# print(df_block["text"].str.lower())
# print(df_block[df_block["text"] == "Curriculum Vitae"]["text"].count())
# print(df_block.loc[df_block["text"] == "Curriculum Vitae"])
# df_block["font-size"] = 0
# df_block.loc[df_block["text"] == "Curriculum Vitae", "font-size"]= 12

# for line in page1.get_text("html").splitlines():
#     soup_line = BeautifulSoup(line, "lxml")
#     spans = soup_line.find_all("span")
#     if spans:
#         b_tag = soup_line.find('b')
#         if b_tag:
#             blocks.append(block_line)
#             block_line = []

#         for span in spans:
#             block_line.append(span.text)
#             # print(span["style"].split(";")[1].replace("font-size:", ""))
#             font_size = span["style"].split(";")[1].replace("font-size:", "")
#             span_text += span.text
#             # print(span_text)
#             # print(df_block[df_block["text"] == span_text])
#             if df_block[df_block["text"] == span_text]["text"].count() == 1:
#                 print("-------------------------------------")
#                 df_block.loc[df_block["text"] == span_text, "font-size"]= font_size
#                 # df_block.loc[span_text]["font-size"] = font_size
#                 font_size = ""
#                 span_text = ""


# blocks.append(block_line)


# for block in blocks:
#     print(block)

# for x in page1.get_text("blocks"):
#     print(x)

# print(df_block)
# for block in page1.get_text("blocks"):
#     print(block)
