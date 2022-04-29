from pathlib import Path
import spacy

model_dir = Path("training/model-last/")
id_nlp = spacy.load(model_dir)

