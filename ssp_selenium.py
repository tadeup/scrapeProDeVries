from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd

url = r"http://www.ssp.sp.gov.br/Estatistica/Pesquisa.aspx/"

driver = webdriver.Firefox(executable_path=r"C:\Users\tadeu\Desktop\FGV\GV DATA\python\scrape\devries\scrapeProDeVries\geckodriver.exe")
driver.get(url)


iteracao = 0
for ano in ["2007", "2005", "2017"]:
    for municipio in range(1,645):
        tentativas = 5
        while tentativas > 0:
            try:
                if iteracao == 50:
                    driver.quit()
                    driver = webdriver.Firefox(executable_path=r"C:\Users\tadeu\Desktop\FGV\GV DATA\python\scrape\devries\scrapeProDeVries\geckodriver.exe")
                    driver.get(url)
                    iteracao = 0
                else:
                    iteracao += 1

                anos = Select(driver.find_element_by_id("conteudo_ddlAnos"))
                anos.select_by_value(str(ano))

                regioes = Select(driver.find_element_by_id("conteudo_ddlRegioes"))
                regioes.select_by_value("0")

                municipios = Select(driver.find_element_by_id("conteudo_ddlMunicipios"))
                municipios.select_by_value(str(municipio))

                #WebDriverWait(driver, 10).until(
                #    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'OCORRÊNCIAS DE PORTE DE ENTORPECENTES')]"))
                #)

                html = driver.page_source
                soup = BeautifulSoup(html,"lxml")
                table = soup.find("tbody").findAll("tr")[1:]

                nome_municipio = soup.find("select", {"id": "conteudo_ddlMunicipios"}).find("option", {"selected": "selected"}).text
                df = pd.DataFrame([{"MUNICIPIO": nome_municipio}])

                for tr in table:
                    elements = tr.findAll("td")
                    x = {elements[0].text: elements[-1].text}
                    foo = pd.DataFrame([x], columns=x.keys())

                    df = pd.concat([df.reset_index(drop=True), foo], axis=1)

                if municipio == 1:
                    df.to_csv(r'csvs/{}.csv'.format(str(ano)), mode='a', header=True)
                else:
                    df.to_csv(r'csvs/{}.csv'.format(str(ano)), mode='a', header=False)
                break
            except Exception as e:
                tentativas -= 1
                print("Erro em municipio: {}; e ano: {}; tentando mais {} vezes".format(municipio, ano, tentativas))
                print(e)
