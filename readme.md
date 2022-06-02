### Now we got UPDATE 3/5/2022
 1. using lebelstudio/work-with-text.py is method to extract text from images to be involved into NER process inside of label studio 0 Natural Language Processing > Named entity recognition Label setup.
 2. inside of label-studio we need to have at least 20 invoices worked for each invoice types, at least at this point we have as example invoices from HIdRO side.  later.. it would depend on our local expert looking examples. From exporting capacities of Lbale-Studio we need to use the one named JSON-MIN, because inside of spacy creation code we defined a specific function for reading that specific data.(spacy/scripts/convert/convertlabelstudiooutput.py), function wich Convert entity annotation from spaCy v2 TRAIN_DATA format to spaCy v3 .spacy format.
 3. we have to run model creation on spacy part of project. The only we have to do is to: a)project.yml- if we want to specify language, gpus, other workflows b)python -m spacy project run all
 4. 




 ### How to run:
1. Everything from requirements have to be installed using 
        pip install -r requirements.txt
        conda install -c conda-forge poppler
        conda install -c conda-forge tesseract 
2. 2.1 create new env for having label-studio in specific place( run following
                                        conda create --name label-studio 
                                        conda activate label-studio 
                                        pip install label-studio
                                                                )
    
    2.2 run in terminal next to open label studio in browser: label-studio start
3. run in terminal next to open local map in localhost for being disponible in web(label-studio): bash labelstudio/serve_local_files.sh ../images 
4. add pdf files into 'pdffiles' map
5. run the next in terminal for creating each page jpg from pdf files : python3 tesseractocr.py
6. in label-studio create new project and add into that json file from images map u have inside of that project localy
7. select the Optical Character Recognition template for your labeling interface. If you want, change the region labels to describe product names and prices, or leave the template with the default region labels of Text and Handwriting.  