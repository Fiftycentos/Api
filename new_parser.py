from bs4 import BeautifulSoup as bs
import pandas as pd

MAIN_URL = 'https://xarid.uzex.uz/info/unfair-executor'

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import selenium
from selenium import webdriver
import time
import sqlite3

con = sqlite3.connect("adata_sqlite_erd.db")
cursor = con.cursor()


path = "C:/Users/Пользователь/PycharmProjects/sql_job_pro/chromedriver.exe"
service = Service(executable_path=path)

def table_parser(driver, df):
    soup = bs(driver, 'html.parser')
    table = soup.find('table')
    for row in table.tbody.find_all('tr'):
        columns = row.find_all('td')
        if (columns != []):
            ID = columns[0].text.strip()
            Organization_name = columns[1].text.strip()
            Full_name = columns[2].text.strip()
            Territory = columns[3].text.strip()
            IIN = columns[4].text.strip()
            Court_decision = columns[5].text.strip()
            Registration_date = columns[6].text.strip()
            Deregistration_date = columns[7].text.strip()

            df = df.append({'ID': ID, 'Organization_name': Organization_name, 'Full_name': Full_name, 'Territory': Territory, 'IIN': IIN,
                            'Court_decision': Court_decision, "Registration_date": Registration_date,
                            "Deregistration_date": Deregistration_date}, ignore_index=True)

    return df



def parser(url):
    df = pd.DataFrame(columns=['ID', 'Organization_name', 'Full_name', 'Territory', 'IIN', 'Court_decision',
                               'Registration_date', 'Deregistration_date' ])

    driver = webdriver.Chrome(service=service)
    driver.get(url)
    time.sleep(2)
    page = driver.find_element(By.CSS_SELECTOR,('.pagination-next .page-link'))

    dfs = [table_parser(driver.page_source, df)]
    while True:
        try:
            page.click()
            time.sleep(1)
            df1 = table_parser(driver.page_source, df)
            dfs.append(df1)
        except selenium.common.exceptions.ElementClickInterceptedException:
            break

    dfs = pd.concat(dfs, ignore_index=True)
    name = 'table_adata.csv'
    dfs.to_csv(name)
    dfs.to_sql('Adata_data_task_2', con, if_exists='replace', index=False)



if __name__ == "__main__":
    parser(MAIN_URL)


"""if __name__ == "__main__":
    start_time = time.time()

    try:
        parser(MAIN_URL)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Parsing completed in {elapsed_time:.2f} seconds")
    except Exception as e:
        print(f"Error during parsing: {str(e)}")"""
