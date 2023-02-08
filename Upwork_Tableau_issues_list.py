import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_data():
    url = f"https://www.tableau.com/support/known-issues?_ga=2.73464402.1191337826.1675669808-625326636.1646950374"
    s = requests.Session()
    r = s.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def issue_id_parse(item):
    try:
        issue_id = item.find('div', {'class': 'field field--name-field-tfs-ids field--node field--label-hidden'}).text.strip()
    except:
        issue_id = ''
    if '\n' in issue_id:
        issue_id = issue_id.replace('\n', ', ')
    return issue_id

def description_parse(item):
    description = item.find('div', {'class': 'field field--name-field-product-known-issue-text field--node field--label-hidden'}).text.replace('\xa0', ' ').strip()
    return description

def product_parse(item):
    product = item.find('span', {'class': 'field field--name-field-products field--node field--label-hidden'}).text.strip()
    if '\n' in product:
        product = product.replace('\n', '')
        while ',  ' in product:
            product = product.replace(',  ', ', ')
    return product
    
def status_parse(item):
    status = item.find('td', {'class': 'text--label table-grid--2 relative'})
    if 'Fixed in' in status.text:
        status_list = status.find('div', {'class': 'field field--name-field-product-versions field--node field--label-hidden'}).text.strip()
        status = "Fixed in: " + status_list.replace('\n', ', ')
    else:
        status = status.text.strip()
    return status
    

def parse(soup):
    table_body = soup.find('tbody')
    rows = table_body.find_all('tr')
    issues_list = []
#     print(rows[2])
    for item in rows:
        data = {
            "ISSUE ID": issue_id_parse(item),
            "PRODUCT": product_parse(item),
            "DESCRIPTION": description_parse(item),
            "STATUS": status_parse(item)
        }
        issues_list.append(data)
#         print(data)
    return issues_list

def output(issues_list):
    issues_df = pd.DataFrame(issues_list)
    issues_df.to_excel('output.xlsx', index=False)

soup = get_data()
issues_list = parse(soup)
output(issues_list)
