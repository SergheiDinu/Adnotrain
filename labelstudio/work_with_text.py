import os
import json
import pytesseract
from PIL import Image
from pathlib import Path

from image_functions import pdf_to_img


def colectandread(map):
    tasks = []
    # collect the receipt images from the image directory

    for f in Path('../'+map).glob('*.jpg'):
        with Image.open(f.absolute()) as image:
            task = pytesseract.image_to_string(image, output_type=pytesseract.Output.DICT)
            tasks.append(task)
    # create a file to import into Label Studio
    with open('../'+map+'/'+'ocr_text.json', mode='w') as f:
        json.dump(tasks, f, indent=2)

if __name__ == '__main__':
    pdf_to_img('pdffiles','images')
    colectandread('images')
