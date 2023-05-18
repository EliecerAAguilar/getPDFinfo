import re
from typing import List, Any
import string


class Tokenizer():
    """clase <Tokenizer>, para la tokenizacion de las palabras y
       el texto de los archivos a procesar
    """

    def __init__(self, input_folder: str, output_folder: str) -> None:
        """El constructor de la clase <Tokenizer>

        :param input_folder: la direccion o Path donde se encuentran los archivos de texto a procesar
        :type input_folder: str
        :param output_folder:la direccion o Path donde se almacenaran los archivos de texto procesados
        :type output_folder: str

        :returns: Nothing
        :rtype: None

        """
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.tokens: List[str] = []

    def standardize(self, raw: Any) -> None:
        """Data cleaning
            elimina los caracteres especiales, los espacios en blanco adicionales,
            simbolos de puntuacion

            :param raw: archivos de con el texto a limpiar
            :type raw: str

            :returns: Nothing
            :rtype: None
        """
        with open(raw, encoding="utf-8") as file:
            contents = file.read()

            # eliminar espacios extra
            contents = re.sub(r"\s+", " ", contents)

            # eliminacion de signos de puntuacion
            contents = re.sub("[^-9A-Za-z]", "", contents)

            # normalizacion de casos
            contents = "".join([_str.lower() for _str in contents if _str not in string.punctuation])

            # tildes, diacriticas, dieresis, virgulilla
            contents = re.sub('á', 'a', contents)
            contents = re.sub('é', 'e', contents)
            contents = re.sub('í', 'i', contents)
            contents = re.sub('ó', 'o', contents)
            contents = re.sub('ú', 'u', contents)
            contents = re.sub('ü', 'u', contents)
            contents = re.sub('ñ', 'n', contents)

        return None


if __name__ == "__main__":
    print("hello.............")
