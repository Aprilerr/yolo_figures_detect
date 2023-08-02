import requests
from pathlib import Path
import re
import json
import os
from config import config as cfg

def parse_paper(file_path, parse_info=""):
    if parse_info == "":
        url = cfg["URL"]["PARSER_URL"]
        with open(file_path, 'rb') as file:
            files = {'file': file}
            response = requests.post(url, files=files)
        text_data = json.loads(response.text)
    else: 
        text_data = json.loads(parse_info)
    text_paragraphs = text_data["pdf_parse"]["body_text"]
    return text_paragraphs

def extract_figure_info(paper_name: str, file_name: str, parse_info:str=""):
    url = cfg["URL"]["PARSER_URL"]  # replace with your URL
    # file_path = './single_example/example.pdf'  # replace with your file path
    folder_path = os.path.join(cfg["SYS"]["OUT"], paper_name)
    path = Path(folder_path)
    file_path = f"{folder_path}.pdf"
    figure_path = path / "figures"

    text_paragraphs = parse_paper(file_path, parse_info)

    for text_file in Path(figure_path).glob("*.txt"):
        with open(str(text_file), 'r+', encoding="utf-8") as f:
            cur_text = f.read()
            match = re.search(r'(\b\w+)\s*\.?\s*(\d+)(?=\D|$)', cur_text)

            if match:
                figure_type, figure_index = match.group(1), match.group(2)

                print(figure_type, figure_index)

                if figure_type.lower().startswith("fig"):
                    pattern = rf"(Figure|Fig\.?\s*)\s*\.?\s*({figure_index})(?=\D|$)"
                else:
                    pattern = rf"({figure_type}s?)\s*\.?\s*({figure_index})(?=\D|$)"

                for item in text_paragraphs:
                    text_match = re.search(pattern, item["text"], re.IGNORECASE)
                    if text_match:
                        f.write(f'\n{item["text"]}')

