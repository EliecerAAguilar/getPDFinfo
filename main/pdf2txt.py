import os
from tika import parser  # https://pypi.org/project/tika/
from typing import List, Any

# Even though it should retun a ByteString, bytes or Buffers, there's no support for those
# kinds of types/values yet... So I would use 'Any'


def read_pdf(pdf_file: str) -> Any:
    """
        read content from pdf files and return it encoded in utf-8
        to avoid special characters problems
    """
    text = parser.from_file(pdf_file)['content']
    return text.encode('utf-8')


def pdf_to_txt(pdf_folder_path: str, txt_folder_path: str) -> None:
    """
    pdf_folder_path: path to your pdf's
    txt_folder_path: path where you want .txt files saved
    """

    pdf_files: List[str] = []

    for root, dirs, files in os.walk(pdf_folder_path):
        for pdf in files:
            if '.pdf' in pdf:
                pdf_files.append(os.path.join(root, pdf))
    # print(pdf_files)

    for pdf_ in pdf_files:
        text_file: str = os.path.splitext(os.path.basename(pdf_))[0]+'.txt'
        with open(os.path.join(txt_folder_path, text_file), 'wb') as text_in_file:
            text_in_file.write(read_pdf(pdf_))

    return None


def main():
    """
        run the script
    """
    pdf_path: str = r"C:\Users\Eliecer\PRISM\text-mining-prism-data\text-mining-prism\estudios"
    txt_path: str = r"C:\Users\Eliecer\PRISM\txt"
    pdf_to_txt(pdf_path, txt_path)


if __name__ == '__main__':
    main()
