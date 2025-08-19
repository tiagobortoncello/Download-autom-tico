import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService

def baixar_proposicoes_almg(ano, tipo_arquivo):
    """
    Função para baixar proposições do ALMG usando Selenium.
    """
    # Configuração do navegador para rodar em modo headless (sem interface gráfica)
    print(f"Iniciando o navegador para baixar o arquivo do ano {ano} no formato {tipo_arquivo}...")
    
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Inicia o serviço do Chrome com o driver gerenciado automaticamente
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        driver.get("https://dadosabertos.almg.gov.br/documentacao/arquivos/proposicoes")

        time.sleep(3) 

        select_ano = Select(driver.find_element(By.ID, "ano"))
        select_ano.select_by_value(ano)

        select_tipo = Select(driver.find_element(By.ID, "tipo"))
        select_tipo.select_by_value(tipo_arquivo)

        botao_baixar = driver.find_element(By.ID, "downloadButton")
        botao_baixar.click()

        print(f"Clique no botão 'Baixar' realizado. Aguardando o download...")
        time.sleep(10)

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    finally:
        driver.quit()
        print("Navegador fechado.")

# Chame a função para rodar o download
# Você pode alterar o ano e o tipo de arquivo aqui
baixar_proposicoes_almg(ano="2024", tipo_arquivo="json")