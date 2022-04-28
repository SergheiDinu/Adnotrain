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