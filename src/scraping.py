from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def iniciar_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--start-maximized")
    
    service = Service(ChromeDriverManager().install())
    
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def acessar_url(driver, url):
    driver.get(url)


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


def main():
    driver = iniciar_driver()
    
    url = "https://www.gov.br/saude/pt-br/assuntos/noticias?b_start:int=0"
    
    acessar_url(driver, url)
    
    time.sleep(5)
    
    cards = coletar_cards(driver)
    print(f"Total de cards encontrados: {len(cards)}")

    for i, card in enumerate(cards[:5]):
        dados = extrair_dados_card(card)
        print(f"\nNotícia {i+1}:")
        print(dados)


    driver.quit()


if __name__ == "__main__":
    main()

