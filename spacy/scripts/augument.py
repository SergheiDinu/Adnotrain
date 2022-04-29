import spacy
import augmenty

nlp = spacy.load('en_core_web_md')

docs = nlp.pipe(['Augmenty is a great tool for text augmentation'])

ent_dict = {'ORG': [['spaCy'], ['spaCy', 'Universe']]}
entity_augmenter = augmenty.load('ents_replace.v1',
                                 ent_dict = ent_dict, level=1)

for doc in augmenty.docs(docs, augmenter=entity_augmenter, nlp=nlp):
    print(doc)