from posixpath import split
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import csv
import os
from http.cookies import SimpleCookie
from termcolor import colored
from os import system
import pandas as pd
from openpyxl import Workbook







print(f"Shutterstock Downloader")

print(f"Criado por andresilvaro@gmail.com")

print(f"Tudo pronto vamos começar")

input(f"Pressione a tecla ENTER para iniciar os Downloads!")



detalhesdousuario0 = []

def read_username(filename):
    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            detalhesdousuario0.append(row[0])

#   Preparação para o login
#    Abra o chrome clique no icone da pessoa ao lado dos três pontos.
#    Clique em adicionar, em seguida clique em continuar sem uma conta e por fim crie um nome para esse novo perfil.
#    Uma nova página do google ira abrir, vá até o site da shutterstock e faça o login, após fazer o login feche o navegador.
#    Abra o arquivo "perfil.csv" e insira a localização da pasta contendo o perfil criado na etapa anterior seguido de ||| nome da pasta aonde foi criado o novo perfil
#    Ex: "C:\Users\Usuario\AppData\Local\Google\Chrome\User Data|||""Profile 1"""
#    Esta etapa só é realiza uma vez
#    No arquivo "codigos.csv" insira o codigo das imagens que deseja licenciar
   
read_username("perfil.csv")





'''abrindo o navegador e logando'''


local_do_perfil = detalhesdousuario0[0].split("|||",1)
nome_do_perfil = local_do_perfil[1].replace('"',"")


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--log-level=3")
chrome_options.add_argument(f'--user-data-dir={local_do_perfil[0]}')
chrome_options.add_argument(f'--profile-directory={nome_do_perfil}')
driver = webdriver.Chrome(options=chrome_options)



driver.get("https://www.shutterstock.com/home")
assert "Shutterstock" in driver.title


'''abrindo o arquivo e lendo os codigos das imagens '''

codigos_das_imagens = []

def read_csv_codigos_das_imagens(filename):
    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            codigos_das_imagens.append(row[0])


read_csv_codigos_das_imagens("codigos.csv")

downloads_num = 0
nondownloads = []
naobaixadas = []
#nao_baixadas("nao_baixadas.csv")

'''para cada codigo de imagem na planilha, abrir o site da shutter e procurar pelo codigo da imagem'''


for codigo in codigos_das_imagens:
    driver.get("https://www.shutterstock.com/search/"+codigo)
    usoeditorial = None
    time.sleep(5) 
    '''procurar pelo texto 'Editorial Use Only.' na página que foi aberta, se encontrar abrir a imagem no modo editor do site'''
    try:
        driver.find_element(By.XPATH,'//*[@id="__next"]/div[2]/div/div[2]/div[1]/div[2]/div/div/div[1]/div[1]/div/div[2]/div/div[2]/div/button').click()
        time.sleep(2) 
        try:
            time.sleep(2)  
            WebDriverWait(driver,1).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(@data-automation, "LicenseDrawer_DownloadButton")]' ))).click()
            success = WebDriverWait(driver,100).until(EC.visibility_of_element_located((By.XPATH, '//h6[contains(text(), "Obrigado!")]' ))).text
            time.sleep(3)
            downloads_num += 1
            index = codigos_das_imagens.index(codigo)
            print(f"Imagem {codigo} baixada com sucesso")
            print(f"Downloads: {downloads_num}/{len(codigos_das_imagens)}")
        except:
            print(f"Verificando se a imagem ja foi baixada anteriormente: {codigo}")
            try:
                time.sleep(2)      
                WebDriverWait(driver,1).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(@data-automation, "LicenseDrawer_ReDownloadButton")]' ))).click()
                success = WebDriverWait(driver,100).until(EC.visibility_of_element_located((By.XPATH, '//h6[contains(text(), "Obrigado!!")]' ))).text
                time.sleep(3)
                downloads_num += 1
                index = codigos_das_imagens.index(codigo)
                print(f"Imagem {codigo} imagem baixada novamente")
                print(f"Downloads: {downloads_num}/{len(codigos_das_imagens)}")
            except:
                nondownloads.append(codigo)
                print(f"Falha de Download: {codigo}")
                pass             
            
    except:
        pass   


df = pd.DataFrame()
df['CODIGOS']=nondownloads

df.to_csv('nao_baixadas.csv', sep=";")




# wait for download complete          

print(f"Finalizado!!!")
print(f"Não foi possível realizar o Download das imagens de código:{nondownloads}")
input(f"Pressione a tecla ENTER para encerrar a aplicação!")
