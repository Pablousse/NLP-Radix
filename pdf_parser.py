import fitz
import pandas as pd


def extract_info_from_page(page_number: int, doc) -> pd.DataFrame:
    """
    Get the text and usefull metadata like font, color... from a pdf page, the metadata will be used to find the titles of sections
    """
    page = doc[page_number]
    df_block = pd.DataFrame(page.get_text("blocks"), columns=["x0", "y0", "x1", "y1", "text", "block_number", "block"])
    df_block["text"] = df_block["text"].replace(r'\n', ' ', regex=True)
    df_block["text"] = df_block["text"].str.strip()

    page_dict = page.get_text("dict")

    font_info = []

    for block in page_dict["blocks"]:
        size = ""
        font = ""
        color = ""
        bold_text = ""
        number = block["number"]
        is_line_bold = 0
        if 'lines' in block.keys():
            for lines in block["lines"]:
                for span in lines["spans"]:
                    if span["text"].strip() != "":
                        size += str(span["size"]) if size == "" else "," + str(span["size"])
                        font += str(span["font"]) if font == "" else "," + str(span["font"])
                        if "bold" in span["font"].lower():
                            bold_text += str(span["text"])
                        color += str(span["color"]) if color == "" else "," + str(span["color"])
        font_info.append([number, size, font, color, is_line_bold, bold_text])

    df_info = pd.DataFrame(font_info, columns=["block_number", "size", "font", "color", "is_line_bold", "bold_text"])
    df_block = df_block.merge(df_info, on="block_number")
    df_block["is_title"] = 0
    df_block["bold_text"] = df_block["bold_text"].str.replace("-", " ").str.replace(":", " ").str.strip()
    df_block.loc[(df_block['text'].str.replace("-", " ").str.replace(":", " ").str.strip().str.split().str.len() < 6) & (df_block["bold_text"] != ""), 'is_title'] = 1

    # Remove empty cells

    df_block = df_block[df_block["text"].replace(" ", "") != ""]

    return pd.DataFrame(df_block)


def extract_info_from_pdf(pdf_path: str) -> pd.DataFrame:
    """
    Get all information from the pdf and output it as a dataframe where each line is a block of text
    """
    doc = fitz.open(pdf_path)

    for i in range(0, len(doc)):
        if i == 0:
            df_informations = extract_info_from_page(i, doc)
        else:
            df_informations = pd.concat([df_informations, extract_info_from_page(i, doc)])

    df_informations = df_informations.reset_index(drop=True)

    return df_informations


def create_sections(pdf_dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Find titles in the pdf text and use it to create sections, also give a category to each section
    """

    objective = ["objective", "synopsis"]
    personnal = ["personnal", "personality", "personal", "about me", "address"]
    education = ["educational", "qualification", "academic", "scholastic", "education"]
    experience = ["experience", "project", "employment", "internship", "training"]
    hobbies = ["hobbies", "curricular", "activity", "activities"]
    skills = ["skill", "computer", "certification", "technical"]
    other = ["strength", "strenth", "strenght", "declaration", "declairation", "achievements"]
    category_list = {"other": other, "personnal": personnal, "hobbies": hobbies, "objective": objective, "skills": skills, "education": education, "experience": experience}
    pdf_dataframe["category"] = ""
    for key, value in category_list.items():
        for category in value:
            pdf_dataframe.at[pdf_dataframe[((pdf_dataframe["bold_text"].str.contains(category, case=False)) | (pdf_dataframe["bold_text"].str.contains((category+"s"), case=False)))].index, "category"] = key

    new_df_array = []
    text = ""
    category = ""
    for index, row in pdf_dataframe.iterrows():
        if text != "" and row["category"] != "":
            new_df_array.append([text, category])
            text = ""
            category = ""
        text += row["text"]
        if row["category"] != "":
            category += row["category"]
    new_df_array.append([text, category])

    return pd.DataFrame(new_df_array, columns=["text", "category"])
