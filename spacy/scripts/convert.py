"""Convert entity annotation from spaCy v2 TRAIN_DATA format to spaCy v3
.spacy format."""
import srsly
import typer
import warnings
from pathlib import Path

import spacy
from spacy.tokens import DocBin


def convert():
    nlp = spacy.blank("eng")
    input_path = '../assets/train.json'
    output_path = '../assets/train.spacy'
    db = DocBin()
    for text, annot in srsly.read_json(input_path):
        doc = nlp.make_doc(text)
        ents = []
        for start, end, label in annot["entities"]:
            span = doc.char_span(start, end, label=label)
            if span is None:
                msg = f"Skipping entity [{start}, {end}, {label}] in the following text because the character span '{doc.text[start:end]}' does not align with token boundaries:\n\n{repr(text)}\n"
                warnings.warn(msg)
            else:
                ents.append(span)
        doc.ents = ents
        db.add(doc)
    db.to_disk(output_path)

def convertlabelstudiooutput(lang: str, input_path: Path, output_path: Path):
    #input_path = '../assets/labelstudiooutput.json'
    #output_path = '../assets/train.spacy'
    nlp = spacy.blank("en")
    db = DocBin()
    for page in srsly.read_json(input_path):
        text = page.get('text')
        doc = nlp.make_doc(text)
        ents = []
        for labels in page.get('label'):
            span = doc.char_span(labels.get('start'), labels.get('end'), label=labels.get('labels')[0])
            if span is None:
                start = labels.get('start')
                end = labels.get('end')
                msg = f"Skipping entity [{start}, {end}, {labels.get('labels')[0]}] in the following text because the character span '{doc.text[start:end]}' does not align with token boundaries:\n\n{repr(text)}\n"
                warnings.warn(msg)
            else:
                ents.append(span)
        doc.ents = ents
        db.add(doc)
    db.to_disk(output_path)

if __name__ == "__main__":
    #typer.run(convert)
    typer.run(convertlabelstudiooutput)
