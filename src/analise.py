import json
import pandas as pd

def carregar_dados():
    with open("noticias.json", "r", encoding="utf-8") as f:
        dados = json.load(f)
    return dados


def criar_dataframe(dados):
    df = pd.DataFrame(dados)
    return df


def tratar_datas(df):
    df["data"] = pd.to_datetime(df["data"], errors="coerce")
    df["ano"] = df["data"].dt.year
    df["dia"] = df["data"].dt.date
    return df


def explodir_tags(df):
    df = df.explode("tags")
    df["tags"] = df["tags"].str.lower()
    return df

    
def main():
    dados = carregar_dados()

    df = criar_dataframe(dados)


if __name__ == "__main__":
    main()