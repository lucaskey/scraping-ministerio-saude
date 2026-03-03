# Scraping de Notícias - Ministério da Saúde

Projeto desenvolvido para coleta e análise de notícias públicas do portal oficial do Ministério da Saúde utilizando Python.


## Objetivo

Realizar o scraping de todas as notícias disponíveis e gerar análises com base em:

- Frequência de termos de tag ao longo dos anos (tags: covid, saúde indígena e sus)
- Tags mais citadas
- Dias com mais notícias


## Tecnologias utilizadas

- Python 3
- Selenium
- Pandas
- Matplotlib


## Como executar o projeto

### 1. Clonar o repositório
```bash
git clone https://github.com/lucaskey/scraping-ministerio-saude.git
cd scraping-ministerio-saude
```

### 2. Criar e ativar ambiente virtual
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar dependências
```bash
pip install -r requirements.txt
```

### 4. Executar o scraping
```bash
python src/scraping.py
```

### 5. Executar as análises
```bash
python src/analise.py
```


## Saídas / Resultados

- Arquivo CSV com os dados coletados
- Gráficos:
  - Frequência de termos de tags por ano
  - Termos mais citados
  - Dias com mais notícias


## Estrutura

```
scraping-ministerio-saude/
├── src/
│   ├── scraping.py
│   └── analise.py
├── data/
├── requirements.txt
├── README.md
└── .gitignore
```


## Observações

- Campos ausentes são tratados como nulos