import pandas as pd


def main() -> None:
    try:
        df = pd.read_csv(
            r"..\csv\00-tabla-hogares-Encuesta de Niveles de Vida 2003.csv")
        print(df.head(10))

    except Exception as e:
        print(e.args)

    return None


if __name__ == "__main__":
    main()
