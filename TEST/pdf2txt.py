#//how to read pdf files and save them into txt files in python?

import os
from tika import parser

def read_pdf(pdf_file):

    text = parser.from_file(pdf_file)['content']
    return text.encode('utf-8')

def pdf_to_txt(folder_with_pdf, dest_folder):

    """

    folder_with_pdf: path to your pdf's
    dest_folder: path where you want .txt files saved

    """

    pdf_files = []

    for root, dirs, files in os.walk(folder_with_pdf):
        for f in files:
            if '.pdf' in f:
                pdf_files.append(os.path.join(root, f))
    #print(pdf_files)

    for file_ in pdf_files:
        text_file = os.path.splitext(os.path.basename(file_))[0]+'.txt'
        with open(os.path.join(dest_folder,text_file), 'wb') as text_f:
            text_f.write(read_pdf(file_))

    return None


def main():
    pdf_path = r"C:\Users\Eliecer\PRISM\text-mining-prism-data\text-mining-prism\estudios"
    txt_path = r"C:\Users\Eliecer\PRISM\txt"
    pdf_to_txt(pdf_path, txt_path) #you should see .txt files being populated in ./txt_folder    


if __name__== '__main__':
    main()
