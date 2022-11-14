from typing import List, Any
from sys import argv
import os
import PyPDF2


# Even though "read_pdf" should retun a ByteString, bytes or Buffers, there's no support for those
# kinds of types/values yet... So I would use 'Any'


class PdfText():
    """
        class to extract text from PDF's files in a folder
        and save them as '.txt' files in another one
    """

    def read_pdf(self, pdf_file: str) -> Any:
        """
            read content from pdf files and return it encoded in utf-8
            to avoid special characters problems
        """

        pdf_reader: str = PyPDF2.PdfReader(pdf_file)
        str_pdf: str = ""

        for x in range(pdf_reader.numPages):
            str_pdf += pdf_reader.pages[x].extract_text()

        return str_pdf.encode("utf-8")

    def pdf_to_txt(self, pdf_folder_path: str, txt_folder_path: str) -> None:
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
                text_in_file.write(self.read_pdf(pdf_))

        return None


def main() -> None:
    """
        run the script
        path where the PDF's files are
        path for the result folder containing the data

    """
    try:
        pdf_path: str = argv[1]
        txt_path: str = argv[2]
        pdf_info = PdfText()
        pdf_info.pdf_to_txt(pdf_path, txt_path)

    except Exception as error_info:
        print(error_info.args)

    return None


if __name__ == '__main__':
    main()
