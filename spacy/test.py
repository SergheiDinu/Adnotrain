
import modelload

nlp = modelload.load("training/model-best/") #load the model
sentence = "I saw Shaka Khan in London."

doc = nlp(sentence)

from modelload import displacy


displacy.render(doc, style="ent", jupyter=True)
print(doc)