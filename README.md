# Desafio Prático Seazone - Analista de Dados Jr

---
O desafio consiste em analisar os dados de ocupação e preço de anúncios no
Airbnb, a fim de responder uma série de perguntas.  
Com o proposito de solucionar o desafio proposto pela [Seazone](https://www.seazone.com.br/) para o processo seletivo da vaga de Analista de Dados Jr.

## Acessar relatório

O app do relatório foi hospedado no Heroku e pode ser acessado atráves do link:

https://seazone-desafio.herokuapp.com/

## Instruções para rodar localmente

### 1 - Fazer um clone do repositório

```git
git clone https://github.com/carlosgsilva/seazone-desafio.git
```

### 2 - Criar um ambiente virtual

O projeto é executado com dependências instaladas em um ambiente virtual. Por favor, crie um antes de instalar.

Para criar um ambiente virtual execute, na raiz do repositório clonado:

``` python
virtualenv -p python3 venv
```

Isso criará uma pasta .venv no diretório raiz que conterá os arquivos de dependência.

Ou use seu fluxo de trabalho de gerenciamento de pacotes preferido. A parte importante é isolar as dependências em um ambiente virtual
ambiente.

### 3 - Ativar ambiente virtual

Para ativar o ambiente virtual execute:

- On Windows

``` sh
.\.venv\Scripts\activate
```

- On Mac or Linux:

```sh
source . venv/bin/activate
```

### 4 - Instalar dependências

Para instalar dependências, execute:

```python
pip3 install -r requirements.txt
```

### 6 - Executando Streamlit

Agora que toda a configuração está concluída, para executar o streamlit, que é a forma escolhida para acessar visualizar o relatório na página web, execute no terminal:

```python
streamlit run report.py
```

Agora o app criado com streamlit pode ser visualizado no navegador nos links:

```sh
Local URL: http://localhost:8501
Network URL: http://192.168.1.10:8501
```