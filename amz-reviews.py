import requests 
import pandas as pd 
from bs4 import BeautifulSoup

url = 'https://www.amazon.it/Philips-hd2581-00-Tostapane-nero/product-reviews/B01N9XBDTI/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews&pageNumber=1'

reviewlist = []


def get_soup(url):

    r = requests.get('http://localhost:8050/render.html', params = {'url': url, 'wait':2})
    soup = BeautifulSoup(r.text, 'html.parser')
    
    return soup 

# does not consider other languages reviews

def get_reviews(soup):
    #print(soup.title.text)
    reviews = soup.find_all('div', {'data-hook': 'review'}) # returns a list
    #print(soup.title.text) 
    try:
        for item in reviews:    
            review = {
            'product' : soup.title.text.replace('Amazon.it:Recensioni clienti:', '') ,
            'title' : item.find('a', {'data-hook': 'review-title'}).text.strip(),
            #rating = item.find('i', {'data-hook': 'review-star-rating-view-point'})
            'rating' : float(item.find('span', {'class': 'a-icon-alt'}).text.replace('su 5 stelle', '').replace(',', '.').strip()),
            'data' : item.find('span', {'class' : 'a-size-base'}).text.replace('Recensito in Italia il ', '').strip(),
            'body' : item.find('span', {'data-hook' : 'review-body'}).text.strip(),  #still to remove some data
            }
            
            reviewlist.append(review)
    except:
        pass


for x in range(1,10): # should be 999 but it is better to not go that further.
    soup = get_soup(f'https://www.amazon.it/Philips-hd2581-00-Tostapane-nero/product-reviews/B01N9XBDTI/ref=cm_cr_getr_d_paging_btm_next_348?ie=UTF8&reviewerType=all_reviews&pageNumber={x}')
    get_reviews(soup)
    if not soup.find('li', {'class': 'a-disabled a-last'}):
        pass
    else:
        break

#soup = get_soup('https://www.amazon.it/Philips-hd2581-00-Tostapane-nero/product-reviews/B01N9XBDTI/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews')
#get_reviews(soup)
df = pd.DataFrame(reviewlist)
df.to_excel('E:/webscraping/Reviews/Toaster-reviews.xlsx', index = False)