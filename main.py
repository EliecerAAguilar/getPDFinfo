from src.Token import Tokenizer


def main() -> None:
    input_folder = r"C:\Users\Eliecer\PRISM\texto"
    output_folder = r"C:\Users\Eliecer\PRISM\token_text"
    token = Tokenizer(input_folder, output_folder)
    token.standardize()



if __name__ == "__main__":
    main()