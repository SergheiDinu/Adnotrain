#File that we gonna use for having functions for extracting text and BBOXES from DocAi
import requests
import unicodedata
import shutil
import pickle
import os
import json
"""
from collections import namedtuple
from pdf2image import convert_from_path
from PyPDF2 import PdfFileWriter, PdfFileReader
from PIL import Image
from glob import glob
"""

print_log = False

from google.cloud import documentai_v1 as documentai

"""#cas_url = Config.CAS_URL
def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                if unicodedata.category(c) != 'Mn')

Rectangle = namedtuple('Rectangle', 'xmin ymin xmax ymax')
def common_area(a, b, tresh):  # returns None if rectangles don't intersect
    dx = min(a.xmax, b.xmax) - max(a.xmin, b.xmin)
    dy = min(a.ymax, b.ymax) - max(a.ymin, b.ymin)
    area_a = (a.xmax - a.xmin)*(a.ymax-a.ymin)
    area_b = (b.xmax - b.xmin)*(b.ymax-b.ymin)
    if (dx>=0) and (dy>=0):
        area = dx*dy
        if area > tresh*area_a and area > tresh*area_b:
            return area


# Save images as pdf files for documentai
def process_image(file, folder, tmp_folder):
    name=file.replace(folder,tmp_folder)
    name=name.replace(".png",".pdf")
    name=name.replace(".jpg",".pdf")
    name=name.replace(".jpeg",".pdf")
    name=name.replace(".gif",".pdf")
    try:
        im1=Image.open(file)
        im1.save(name,save_all=True)
    except Exception as e:
        if print_log: print(f"Couldn't transform {file} to pdf: {e}")

#change PDF into series of images
def extract_pdf(file, tmp_folder):
    filename=file.split("/")[-1]
    if print_log: print("Saving images from {}\n".format(filename))
    try:
        images = convert_from_path(file)
        if print_log: print("Got {} images\n".format(len(images)))
    except:
        if print_log: print("Cannot convert images from pdf {}\n".format(file))
    try:
        front=tmp_folder+"/"+filename.replace(".pdf","")
        for i in range(len(images)):
            temp=front+ str(i) +'.png'
            images[i].save(temp)
            if print_log: print("Successfuly saved image {}\n".format(temp))
    except:
        if print_log: print("Cannot save image {}\n".format(file))

def get_gcp_ocr(file, path):

    try:
        doc = ocr_factura(file_path=file)
    except Exception as excpt:
        if print_log: print(f"Failed to ocr {file} : {excpt}")

    file=path+"/ocr_extracted.txt"

    if os.path.exists(file):
        append_write = 'a' # append if already exists
    else:
        append_write = 'w' 
    fout=open(file,append_write)
    fout.write("\n")
    fout.write(doc.text)
    fout.close();

    return doc

def process_facturi(folder, tmp_folder):
    file=glob(tmp_folder+"/*.pdf")[0]
    filename = file.split("/")[-1]
    folder_name = folder.split("/")[-1]

    inputpdf = PdfFileReader(open(file, "rb"),strict=False)
    print(f"{filename} have {inputpdf.getNumPages()} pages!")
    if inputpdf.getNumPages() > 10:
        os.remove(file)
        file = file.replace(".pdf","_10.pdf")
        output = PdfFileWriter()
        for i in range(10):
            output.addPage(inputpdf.getPage(i))
        with open(file, "wb") as outputStream:
            output.write(outputStream)

    doc = get_gcp_ocr(file, tmp_folder)
    for page in doc.pages:
        page.image.content = b''
    with open(tmp_folder+'/documentai.gcp', 'wb') as f:
        pickle.dump(doc, f)
    
    prepare_tmp(folder, 'pages')
    images = convert_from_path(file)
    for i, page in enumerate(doc.pages):
    
        if len(page.tokens) > 0:
            images[i].save(folder + "/pages/" + folder_name + "_" + str(i) + ".jpg")

            index = 0
            tasks = []
            predictions = []
            result = []
            word_list = []
            full_text = ""

            page_width, page_height = images[i].size

            for token in page.tokens:
                value = {}
                token_text_list = []
                index+=1
                for ts in token.layout.text_anchor.text_segments:
                    token_text = doc.text[ts.start_index:ts.end_index].replace("\n","").replace("\u2022","*").rstrip()
                    token_text_list.append(strip_accents(token_text))

                current_dict = {}
                location_dict = {}
                location_dict ['start'] = len(full_text)
                location_dict ['lenght'] = len(token_text)
                location_dict ['stop'] = len(full_text)+len(token_text)
                current_dict ['id'] = index
                current_dict ['location'] = location_dict
                word_list.append(current_dict)

                full_text += strip_accents(token_text)
                if str(token.detected_break.type_) != 'Type.TYPE_UNSPECIFIED' and str(token.detected_break.type_) != 'Type.HYPHEN':
                    full_text += " "

                token_x = []
                token_y = []
                for nv in token.layout.bounding_poly.normalized_vertices:
                    
                    # Absolute values
                    token_x.append(page_width*nv.x)
                    token_y.append(page_height*nv.y)
                    
                value['text'] = token_text_list
                value['x'] = min(token_x)
                value['y'] = min(token_y)
                value['width'] = max(token_x)-min(token_x)
                value['height'] = max(token_y)-min(token_y)
                value['rotation'] = 0
                result.append({
                    'id': index,
                    'length': len(token_text),
                    'value': value,
                    'score': token.layout.confidence
                })

            predictions.append({'result': result})
            tasks.append({'data': {'ocr': file}, 'predictions': predictions})

            text_boxes_list = []
            fields_list = []
            for l in LABELS:
                fields_list.append({"field_name": l,
                                    "value_id": [],
                                    "value_text": [],
                                    "key_id": [],
                                    "key_text": []})
            index = 0
            for task in tasks:
                for prediction in task.get('predictions'):
                    for item in prediction.get('result'):
                        index += 1
                        current_item_dict = {}
                        current_item_dict['id'] = index
                        locations = []
                        locations.append(item.get('value').get('x'))
                        locations.append(item.get('value').get('y'))
                        locations.append(item.get('value').get('x')+item.get('value').get('width'))
                        locations.append(item.get('value').get('y')+item.get('value').get('height'))
                        current_item_dict['bbox'] = locations
                        current_item_dict['text'] = " ".join(item.get('value').get('text'))
                        text_boxes_list.append(current_item_dict)
            
            CUTIE_JSON = {
                'text_boxes': text_boxes_list,
                'fields': fields_list,
                'global_attributes': {
                    'file_id': folder_name+ "_" + str(i) +".jpg"
                }
            }

            with open(folder+ "/pages/" + folder_name + "_" + str(i) + ".json", mode='w') as f:
                json.dump(CUTIE_JSON, f, indent=2)

    outputs_folder = prepare_tmp(folder, 'outputs')
    tmpFactura = Factura()
    cutie_predict(folder_name, outputs_folder)

    cur_dict, output_dict, adresa_cas = merge_pages(glob(folder+"/outputs/*.json"), do_split_address=True)
    print(output_dict)
    values = []
    for k,v in output_dict.items():
        values.append((0.69,k,v))
    tmpFactura.setParam(values)

    if len(tmpFactura.furnizor) != 0:
        imgs_path = tmp_folder.replace("pdfs","imgs")
        files=glob(imgs_path+"/*.*")
        for i, file in enumerate(files):
            files[i] = file.split("/")[-1]
        tmpFactura.setFisiere(imgs_path,files)
    
    with open(folder + "/cutie_output.json", mode='w') as f:
        json.dump(tmpFactura.toJSON(), f, indent=2)

    return tmpFactura.toJSON()


"""
def ocr_factura(file_path: str):
    project_id = "hidroelectrica"#Config.project_id
    location = "eu"#Config.location
    processor_id = "69db52413ef8723"#Config.processor_id
    if print_log: print(f"\nProcessing factura {file_path}")
    opts = {}
    if location == location:
        opts = {"api_endpoint": "eu-documentai.googleapis.com"}
    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    name = f"projects/{project_id}/locations/{location}/processors/{processor_id}"

    # Read the file into memory
    with open(file_path, "rb") as image:
        image_content = image.read()

    document = {"content": image_content, "mime_type": "application/pdf"}

    # Configure the process request
    request = {"name": name, "raw_document": document}

    result = client.process_document(request=request)
    document = result.document

    return document

if __name__ == '__main__':
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="../docai.json"
    ocr_factura("file.jpg")
