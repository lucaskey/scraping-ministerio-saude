import json
import pandas as pd

def carregar_dados():
    with open("noticias.json", "r", encoding="utf-8") as f:
        dados = json.load(f)
    return dados

def criar_dataframe(dados):
    df = pd.DataFrame(dados)
    return df
    
def main():
    dados = carregar_dados()

    df = criar_dataframe(dados)

    print(df.head())

if __name__ == "__main__":
    main()