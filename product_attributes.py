from matplotlib.pyplot import table
import requests 
import pandas as pd 
from bs4 import BeautifulSoup


url = 'https://www.amazon.it/Philips-hd2581-00-Tostapane-nero/dp/B01N9XBDTI/ref=sr_1_5?__mk_it_IT=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=26VHA14FAG6ZX&keywords=toaster&qid=1648288905&sprefix=toaster%2Caps%2C80&sr=8-5&th=1'

def scrape_amz_tables(url): 
    # Use splash to scrape the web 
    r = requests.get('http://localhost:8050/render.html', params = {'url': url, 'wait':2})
    soup = BeautifulSoup(r.text, 'html.parser')

    # find the table
    table_attrib = soup.find('table', {'id': 'productDetails_techSpec_section_1'})
    
    col_names = []
    dati_tab = []
    # iterate along all the columns of the table
    for row in table_attrib.tbody.find_all('tr'):
        dati = row.text.replace('\u200e', '')
        dati = ' '.join(dati.split())
        ind_split = dati.find(' ')
        col_names.append(dati[:ind_split])                  
        dati_tab.append(dati[ind_split+1 :])   

    average_rating = float((soup.find('span', {'class' : 'a-icon-alt'}).text).replace(' su 5 stelle', '').replace(',', '.'))
    col_names.append('Average Rating')
    dati_tab.append(average_rating)
    df = pd.DataFrame([dati_tab], columns= col_names)
    df.to_excel('E:/webscraping/tab_prod.xlsx')


scrape_amz_tables(url)