from simple_salesforce import Salesforce
import requests
import csv
import pandas as pd
from openpyxl import Workbook
import os
from urllib.parse import urljoin

# Substitua pelas suas credenciais do Salesforce
username = 'your_username'
password = 'your_password'
security_token = 'your_security_token'

# ID do relatório que você deseja baixar
report_id = 'your_report_id'

# Inicialize a conexão com o Salesforce
sf = Salesforce(username=username, password=password, security_token=security_token)

try:
    # Consulte o relatório para obter seu nome
    report = sf.get_report(report_id)
    report_name = report['Name']

    # Gere o URL de download do relatório em formato CSV
    report_url = urljoin(sf.base_url, f"/analytics/reports/{report_id}?format=csv")

    # Faça o download do relatório em formato CSV
    response = requests.get(report_url, headers=sf.headers)
    response.raise_for_status()  # Lança uma exceção para códigos de erro HTTP

    # Salve o arquivo CSV localmente
    csv_filename = f'{report_name}.csv'
    with open(csv_filename, 'wb') as csv_file:
        csv_file.write(response.content)

    # Converta o arquivo CSV para XLSX
    df = pd.read_csv(csv_filename)
    xlsx_filename = f'{report_name}.xlsx'
    df.to_excel(xlsx_filename, index=False, engine='openpyxl')

    print(f"Relatório '{report_name}' baixado com sucesso como '{xlsx_filename}'")

except Exception as e:
    print(f"Erro ao baixar o relatório '{report_name}': {str(e)}")
