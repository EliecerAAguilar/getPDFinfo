import os
from tika import parser #https://pypi.org/project/tika/

def read_pdf(pdf_file):
    """
        read content from pdf files and return it encoded in utf-8
        to avoid special characters problems
    """
    text = parser.from_file(pdf_file)['content']
    return text.encode('utf-8')

def pdf_to_txt(pdf_folder_path, txt_folder_path):
    """
    pdf_folder_path: path to your pdf's
    txt_folder_path: path where you want .txt files saved
    """

    pdf_files = []

    for root, dirs, files in os.walk(pdf_folder_path):
        for file in files:
            if '.pdf' in file:
                pdf_files.append(os.path.join(root, file))
    #print(pdf_files)

    for file_ in pdf_files:
        text_file = os.path.splitext(os.path.basename(file_))[0]+'.txt'
        with open(os.path.join(txt_folder_path,text_file), 'wb') as text_in_file:
            text_in_file.write(read_pdf(file_))

    return None


def main():
    """
        run the script
    """    
    pdf_path = r"C:\Users\Eliecer\PRISM\text-mining-prism-data\text-mining-prism\estudios"
    txt_path = r"C:\Users\Eliecer\PRISM\txt"
    pdf_to_txt(pdf_path, txt_path)


if __name__== '__main__':
    main()
