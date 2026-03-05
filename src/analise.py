import json
import pandas as pd
import matplotlib.pyplot as plt

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


def grafico_evolucao(df):
    termos = ["covid", "sus", "saúde indígena"]

    df_filtrado = df[df["tags"].isin(termos)]

    resultado = df_filtrado.groupby(["ano", "tags"]).size().unstack(fill_value=0)

    resultado.plot(kind="line", marker="o")
    plt.title("Evolução de Tags por Ano")
    plt.xlabel("Ano")
    plt.ylabel("Quantidade")
    plt.grid()

    plt.show()
    
    
def grafico_tags(df):
    top_tags = df["tags"].value_counts().head(20)[::-1]

    plt.figure(figsize=(12, 8))
    ax = top_tags.plot(kind="barh") 

    for bar in ax.patches:
        val = int(bar.get_width())
        ax.text(
            bar.get_width() + 1,          
            bar.get_y() + bar.get_height() / 2, 
            str(val),                     
            va="center", fontsize=9
        )
        
    plt.title("Top 20 Termos Mais Citados nas Tags")
    plt.xlabel("Tag")
    plt.ylabel("Frequência")

    plt.show()
    
    
def main():
    dados = carregar_dados()

    df = criar_dataframe(dados)
    
    df = tratar_datas(df)
    df = explodir_tags(df)

    # grafico_evolucao(df)
    grafico_tags(df)


if __name__ == "__main__":
    main()