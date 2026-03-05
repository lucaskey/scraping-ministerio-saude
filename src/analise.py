import json
import pandas as pd
import matplotlib.pyplot as plt
import os

ARQUIVO_JSON = "data/noticias.json"
PASTA_SAIDA  = "data"

def carregar_dados(caminho=ARQUIVO_JSON):
    with open(caminho, "r", encoding="utf-8") as f:
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
    plt.tight_layout()

    plt.savefig("data/grafico_evolucao_tags.png", dpi=150)
    plt.close()
    
    
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
    plt.xlabel("Frequência")
    plt.ylabel("Tag")
    plt.tight_layout()

    plt.savefig("data/grafico_termos_mais_citados.png", dpi=150)
    plt.close()
    

def grafico_dias(df):
    noticias_por_dia = df.groupby("dia").size().sort_values(ascending=False).head(20)

    plt.figure(figsize=(14, 6))
    ax = noticias_por_dia.plot(kind="bar", width=0.85)
    for bar in ax.patches:
        val = int(bar.get_height())
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.1,            
            str(val),
            ha="center", fontsize=9
        )
    plt.title("Quantidade de Notícias por Dia")
    plt.xlabel("Data")
    plt.ylabel("Quantidade")
    plt.xticks(rotation=45, ha="right", fontsize=9)
    plt.grid(axis="y", linestyle="--", alpha=0.4)
    plt.tight_layout()

    plt.savefig("data/grafico_dias.png", dpi=150)
    plt.close()
    
    
def main():
    print("Carregando dados...")
    dados = carregar_dados()
    df = criar_dataframe(dados) 
    df = tratar_datas(df)
    df_original = df.copy()
    df_tags = explodir_tags(df)

    print("Gerando gráficos...")
    os.makedirs(PASTA_SAIDA, exist_ok=True)
    grafico_evolucao(df_tags)
    grafico_tags(df_tags)
    grafico_dias(df_original)
    print("Concluído! Gráficos salvos em data/")


if __name__ == "__main__":
    main()