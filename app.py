import psycopg2
import os
from time import sleep
from datetime import datetime, timezone
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as codicao_esperada
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import *


conexao = psycopg2.connect(
    database=os.environ.get('DB_NAME'),
    user=os.environ.get('DB_USER'),
    password=os.environ.get('DB_PASSWORD'),
    host=os.environ.get('DB_HOST'),
    port=os.environ.get('DB_PORT')
)
sql = conexao.cursor()

def novo_produto(sql, conexao, nome, preco, site, data_cotacao, link_imagem):
    query = 'SELECT * FROM buscapreco_produto WHERE nome=%s and preco=%s and site=%s'
    valores = (nome, preco, site)
    resultado = sql.execute(query, valores)
    dados = sql.fetchall()

    if not len(dados) == 0:
        print('Dados já cadastrados anteriormente!')

    query = 'INSERT INTO buscapreco_produto (nome, preco, site, data_cotacao, link_imagem) VALUES(%s,%s,%s,%s,%s)'
    valores = (nome, preco, site, data_cotacao, link_imagem)
    sql.execute(query, valores)

    conexao.commit()


def iniciar_driver():
    firefox_options = Options()
    arguments = ('--lang=en-US', 'window-size=1920,1080',
                 '--incognito')
    for argument in arguments:
        firefox_options.add_argument(argument)
    
    firefox_options.add_experimental_option('prefs', {
        'download.prompt_for_download': False,
        'profile.default_content_setting_values.notifications': 2,
        'profile.default_content_setting_values.automatic_downloads': 1
    })

    driver = webdriver.Firefox(service=FirefoxService(
        GeckoDriverManager().install()), options=firefox_options)
    wait = WebDriverWait(
        driver,
        10,
        poll_frequency=1,
        ignored_exceptions=[
            NoSuchElementException,
            ElementNotVisibleException,
            ElementNotSelectableException,
        ]
    )
    return driver, wait

def varrer_site_1():
    driver, wait = iniciar_driver()
    driver.get('https://site1produto.netlify.app/')
    nomes = wait.until(codicao_esperada.visibility_of_all_elements_located((By.XPATH,"//div[@class='detail-box']/a")))
    precos = wait.until(codicao_esperada.visibility_of_all_elements_located((By.XPATH,"//h6[@class='price_heading']")))
    site = driver.current_url
    links_imagem = wait.until(codicao_esperada.visibility_of_all_elements_located((By.XPATH,"//div[@class='img-box']/img")))

    nome_iphone = nomes[0].text
    nome_gopro = nomes[1].text

    preco_iphone = precos[0].text.split(' ')[1]
    preco_gopro = precos[1].text.split(' ')[1]

    link_imagem_iphone = links_imagem[0].get_attribute('src')
    link_imagem_gopro = links_imagem[1].get_attribute('src')

    novo_produto(sql, conexao, nome_iphone, preco_iphone, site, datetime.now(), link_imagem_iphone)
    novo_produto(sql, conexao, nome_gopro, preco_gopro, site, datetime.now(), link_imagem_gopro)

def varrer_site_2():
    ...

def varrer_site_3():
    ...