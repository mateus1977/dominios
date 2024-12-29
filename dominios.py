import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sqlite3
import pandas as pd
from datetime import datetime

# Configuração do banco de dados SQLite
DATABASE = 'dominios.db'

def create_table():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dominios (
                domain TEXT PRIMARY KEY,
                status TEXT,
                last_updated TIMESTAMP,
                created TEXT,
                changed TEXT,       
                expiration TEXT,
                email TEXT       
            )
        ''')
        conn.commit()

def get_status_for_domain(driver, domain):
    driver.get('https://registro.br/tecnologia/ferramentas/whois/')
    input_register = driver.find_element(By.ID, 'whois-field')
    input_register.clear()
    input_register.send_keys(domain)
    enviar = driver.find_element(By.CSS_SELECTOR, 'form button[type="submit"]')
    enviar.click()
    wait = WebDriverWait(driver, 10)
    status = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.cell-status')))
    created_hash = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.cell-createdat')))
    changed = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.cell-updatedat')))
    expiration = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.cell-expiresat')))
    created = created_hash.text.split('#')[0].strip()
    return domain, status.text, created, changed.text, expiration.text

def read_domains_from_excel(filename):
    # Lê o arquivo Excel
    df = pd.read_excel(filename)
    
    # Converte para uma lista de dicionários
    domains = df.to_dict(orient='records')
    return domains

def update_database(domains_status):
    timestamp = datetime.now().strftime('%d-%m-%Y')
    
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.executemany('''
            INSERT INTO dominios (domain, status, last_updated, created, changed, expiration, email)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(domain) DO UPDATE SET
                status=excluded.status,
                last_updated=excluded.last_updated,
                created=excluded.created,
                changed=excluded.changed,
                expiration=excluded.expiration,
                email=excluded.email
        ''', [(domain, status, timestamp, created, changed, expiration, email) for domain, status, created, changed, expiration, email in domains_status])
        conn.commit()

def fetch_from_database():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
                            SELECT domain, status, created, changed, expiration, email 
                            FROM dominios 
                            ORDER BY STRFTIME('%Y-%m-%d', SUBSTR(expiration, 7, 4) || '-' || SUBSTR(expiration, 4, 2) || '-' || SUBSTR(expiration, 1, 2)) ASC
                        """)
        return cursor.fetchall()

# Cria a tabela se não existir
create_table()

# Função para obter e exibir os resultados atualizados
def get_results():
    return fetch_from_database()

# Interface do Streamlit
st.title("Status dos Domínios - Registro.br")

# Carregar domínios de um arquivo Excel
domains_file = 'dominios.xlsx'
domains = read_domains_from_excel(domains_file)

# Adiciona um botão para obter o status
if st.button('Obter Status'):
    with st.spinner('Obtendo dados...'):
        driver = webdriver.Chrome()
        domains_status = []
        try:
            for entry in domains:  
                domain = entry['dominio']  
                email = entry['email']  
                value, status_text, created_text, changed_text, expiration_text = get_status_for_domain(driver, domain)
                domains_status.append((value, status_text, created_text, changed_text, expiration_text, email))
        finally:
            driver.quit()
        
        # Atualiza o banco de dados
        update_database(domains_status)

# Exibe os dados armazenados no banco de dados em formato de DataFrame
results = get_results()

# Exibe a data e hora da última atualização (se disponível)
def fetch_timestamp():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT last_updated FROM dominios')
        return cursor.fetchall()
    
result_last_time = fetch_timestamp()

if result_last_time:
    last_update_time = result_last_time[0][0]  
else:
    last_update_time = 'N/A'

st.subheader(f"Última Atualização da Página: {last_update_time}")

# Cria o DataFrame
df = pd.DataFrame(results, columns=['Dominio', 'Status', 'Criado', 'Alterado', 'Expirado', 'email'])

# Formatação de cores para a coluna de Status
def color_status(val):
    color = 'green' if 'publicado' in val.lower() else 'red' if 'congelado' in val.lower() else 'black'
    return f'color: {color}'

# Aplica a formatação ao DataFrame
styled_df = df.style.applymap(color_status, subset=['Status'])

# Exibe a tabela
st.dataframe(styled_df)
