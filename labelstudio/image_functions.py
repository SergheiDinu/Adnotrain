from pdf2image import convert_from_path
import os

def pdf_to_img(map,tomap):
    for i in os.scandir('../'+map):
        name='../'+tomap+"/"+i.name.replace(".pdf","")
        #print(name)
        images = convert_from_path(i)
        for i in range(len(images)):
            # Save pages as images in the pdf
            images[i].save(name+'_'+str(i) +'.jpg', 'JPEG')

if __name__ == '__main__':
    pdf_to_img('pdffiles','images')
    