import psycopg2
import os
from time import sleep
from datetime import datetime, timezone
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as codicao_esperada
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import *
import schedule


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
        return 0

    query = 'INSERT INTO buscapreco_produto (nome, preco, site, data_cotacao, link_imagem) VALUES(%s,%s,%s,%s,%s)'
    valores = (nome, preco, site, data_cotacao, link_imagem)
    sql.execute(query, valores)

    conexao.commit()


def iniciar_driver():
    chrome_options = Options()
    arguments = ('--lang=en-US', 'window-size=1920,1080',
                 '--incognito', '--headless')
    for argument in arguments:
        chrome_options.add_argument(argument)
    
    chrome_options.add_experimental_option('prefs', {
        'download.prompt_for_download': False,
        'profile.default_content_setting_values.notifications': 2,
        'profile.default_content_setting_values.automatic_downloads': 1
    })

    driver = webdriver.Chrome(service=ChromeService(
        ChromeDriverManager().install()), options=chrome_options)
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

    novo_produto(sql, conexao, nome_iphone, float(preco_iphone), site, datetime.now(), link_imagem_iphone)
    novo_produto(sql, conexao, nome_gopro, float(preco_gopro), site, datetime.now(), link_imagem_gopro)

def varrer_site_2():
    driver, wait = iniciar_driver()
    driver.get('https://site2produto.netlify.app/')
    nomes = wait.until(codicao_esperada.visibility_of_all_elements_located((By.XPATH,"//div[@class='why-text']")))
    precos = wait.until(codicao_esperada.visibility_of_all_elements_located((By.XPATH,"//div[@class='why-text']//h5")))
    links_imagem = wait.until(codicao_esperada.visibility_of_any_elements_located((By.XPATH,"//img[@class='img-fluid']")))
    site = driver.current_url

    nome_iphone = nomes[0].text.split('\n')[0]
    nome_gopro = nomes[1].text.split('\n')[0]

    preco_iphone = precos[0].text.split('$')[1]
    preco_gopro = precos[1].text.split('$')[1]

    link_imagem_iphone = links_imagem[0].get_attribute('src')
    link_imagem_gopro = links_imagem[1].get_attribute('src')

    novo_produto(sql, conexao, nome_iphone, float(preco_iphone), site, datetime.now(), link_imagem_iphone)
    novo_produto(sql, conexao, nome_gopro, float(preco_gopro), site, datetime.now(), link_imagem_gopro)

def varrer_site_3():
    driver, wait = iniciar_driver()
    driver.get('https://site3produto.netlify.app/')
    nomes = wait.until(codicao_esperada.visibility_of_all_elements_located((By.XPATH,"//div[@class='product__item__text']//h6/a")))
    precos = wait.until(codicao_esperada.visibility_of_all_elements_located((By.XPATH,"//div[@class='product__item__text']//h5")))
    links_imagem = wait.until(codicao_esperada.visibility_of_all_elements_located((By.XPATH,"//div[@class='product__item__pic set-bg']")))
    site = driver.current_url

    nome_iphone = nomes[0].text[0]
    nome_gopro = nomes[1].text[0]

    preco_iphone = precos[0].text.split('$')[1]
    preco_gopro = precos[1].text.split('$')[1]

    link_imagem_iphone = driver.current_url+links_imagem[0].get_attribute('style').split(' ')[1][5:-3]
    link_imagem_gopro = driver.current_url+links_imagem[1].get_attribute('style').split(' ')[1][5:-3]

    novo_produto(sql, conexao, nome_iphone, float(preco_iphone), site, datetime.now(), link_imagem_iphone)
    novo_produto(sql, conexao, nome_gopro, float(preco_gopro), site, datetime.now(), link_imagem_gopro)

def rodar_tarefas():
    varrer_site_1()
    varrer_site_2()
    varrer_site_3()

# schedule.every.day.at('06:00').do(rodar_tarefas)
schedule.every(1).seconds.do(rodar_tarefas)

while True:
    schedule.run_pending()
    sleep(1)