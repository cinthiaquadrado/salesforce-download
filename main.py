from simple_salesforce import Salesforce
import requests
import csv
import pandas as pd
from openpyxl import Workbook

# Substitua pelas suas credenciais do Salesforce
username = 'your_username'
password = 'your_password'
security_token = 'your_security_token'

# IDs dos relatórios que você deseja baixar
report_ids = ['report_id_1', 'report_id_2', 'report_id_3']

# Inicialize a conexão com o Salesforce
sf = Salesforce(username=username, password=password, security_token=security_token)

for report_id in report_ids:
    # Consulte o relatório para obter seu nome
    report = sf.Report.get(report_id)
    report_name = report['Name']

    # Gere o URL de download do relatório em formato CSV
    report_url = sf.base_url + f"/analytics/reports/{report_id}?format=csv"

    # Faça o download do relatório em formato CSV
    response = requests.get(report_url, headers=sf.headers)
    if response.status_code == 200:
        # Salve o arquivo CSV localmente
        with open(f'{report_name}.csv', 'wb') as csv_file:
            csv_file.write(response.content)

        # Converta o arquivo CSV para XLSX
        df = pd.read_csv(f'{report_name}.csv')
        df.to_excel(f'{report_name}.xlsx', index=False, engine='openpyxl')

        print(f"Relatório '{report_name}' baixado com sucesso como '{report_name}.xlsx'")
    else:
        print(f"Erro ao baixar o relatório '{report_name}'. Status Code: {response.status_code}")
