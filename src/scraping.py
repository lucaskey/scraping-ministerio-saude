from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
import os

def iniciar_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--start-maximized")
    
    service = Service(ChromeDriverManager().install())
    
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def coletar_cards(driver):
    cards = driver.find_elements(By.CLASS_NAME, "tile-collective-nitf-content")
    return cards


def extrair_dados_card(card):
    try:
        chamada = card.find_element(By.CLASS_NAME, "subtitle").text
    except:
        chamada = None
        
    try:
        titulo = card.find_element(By.CLASS_NAME, "tileHeadline").text
    except:
        titulo = None
        
    try:
        subtitulo = card.find_element(By.CLASS_NAME, "tileBody").text
    except:
        subtitulo = None
        
    try:
        tags_elements = card.find_elements(By.CSS_SELECTOR, ".keywords a")
        tags = [tag.text.strip() for tag in tags_elements]
    except:
        tags = []
        
    try:
        data = card.find_element(By.CLASS_NAME, "summary-view-icon").text
    except:
        data = None
    
    return {
        "chamada": chamada,
        "titulo": titulo,
        "subtitulo": subtitulo,
        "tags": tags,
        "data": data
    }


def coletar_noticias_pagina(driver):
    cards = coletar_cards(driver)
    
    noticias = []
    
    for card in cards:
        dados = extrair_dados_card(card)
        noticias.append(dados)
        
    return noticias


def coletar_todas_noticias(driver):
    base_url = "https://www.gov.br/saude/pt-br/assuntos/noticias?b_start:int=0"
    
    todas_noticias = []
    pagina = 0
    titulos_vistos = set()

    while True:
        url = base_url + str(pagina)
        print(f"Acessando página {pagina}")

        driver.get(url)
        time.sleep(4)

        cards = coletar_cards(driver)

        if not cards:
            break

        novos = 0

        for card in cards:
            dados = extrair_dados_card(card)

            if dados["titulo"] not in titulos_vistos:
                titulos_vistos.add(dados["titulo"])
                todas_noticias.append(dados)
                novos += 1

        if novos == 0:
            print("Nenhuma notícia nova encontrada. Encerrando...")
            break

        pagina += 30

    return todas_noticias


def salvar_json(noticias, caminho="data/noticias.json"):
    os.makedirs("data", exist_ok=True)
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(noticias, f, ensure_ascii=False, indent=2)
    print(f"Dados salvos em {caminho}")


def main():
    driver = iniciar_driver()
    
    try:
        noticias = coletar_todas_noticias(driver)
    finally:
        driver.quit()
        
    print(f"Total coletado: {len(noticias)}")
    
    salvar_json(noticias)


if __name__ == "__main__":
    main()

