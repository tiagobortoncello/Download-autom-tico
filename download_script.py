import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
import os
import datetime

def baixar_proposicoes_almg(ano, tipo_arquivo):
    """
    Função para baixar proposições do ALMG usando Selenium.
    """
    # Define a pasta de downloads dentro do ambiente de execução
    downloads_folder = os.path.join(os.getcwd(), 'downloads')
    if not os.path.exists(downloads_folder):
        os.makedirs(downloads_folder)

    # Configuração do navegador para rodar em modo headless e salvar no diretório
    print(f"Iniciando o navegador para baixar o arquivo do ano {ano} no formato {tipo_arquivo}...")
    
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": downloads_folder,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True
    })

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        driver.get("https://dadosabertos.almg.gov.br/documentacao/arquivos/proposicoes")
        time.sleep(5) 

        select_ano = Select(driver.find_element(By.ID, "ano"))
        select_ano.select_by_value(ano)

        select_tipo = Select(driver.find_element(By.ID, "tipo"))
        select_tipo.select_by_value(tipo_arquivo)

        botao_baixar = driver.find_element(By.ID, "downloadButton")
        botao_baixar.click()

        print(f"Clique no botão 'Baixar' realizado. Aguardando o download...")
        time.sleep(15) 

        # Renomeia o arquivo baixado com a data atual para evitar sobrescrever
        arquivos_baixados = os.listdir(downloads_folder)
        if arquivos_baixados:
            nome_original = arquivos_baixados[0]
            data_atual = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            nome_novo = f"proposicoes_{ano}_{tipo_arquivo}_{data_atual}.zip"
            os.rename(os.path.join(downloads_folder, nome_original), os.path.join(downloads_folder, nome_novo))
            print(f"Arquivo renomeado para: {nome_novo}")
        else:
            print("Nenhum arquivo encontrado na pasta de downloads.")

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    finally:
        driver.quit()
        print("Navegador fechado.")

# Chame a função para rodar o download
baixar_proposicoes_almg(ano="2024", tipo_arquivo="json")
