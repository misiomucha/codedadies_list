from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from requests.compat import quote_plus
from . import models


BASE_CRAIGSLIST_URL = 'https://warsaw.craigslist.org/search/hhh?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'

def home(request):
    return render(request, template_name='base.html')

def new_search(request):
    search = request.POST.get('search')
    #bierzemy dane z zemiennej search i tworzymy w bazie(objekcie) modelu Search
    models.Search.objects.create(search=search)
    #print(quote_plus(search))
    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search))
    #modyfikuje url do {} dodaje to co jest w search oraz dodaje plusy tam gdzie sa spacje quote_plus
    #print(final_url)
    #response = requests.get('https://warsaw.craigslist.org/search/jjj?query=train&sort=rel')
    response = requests.get(final_url)
    data = response.text
    #print(data)
    soup = BeautifulSoup(data, features='html.parser')
    #post_titles = soup.find_all('a', {'class': 'result-title'})
    post_listings = soup.find_all('li', {'class': 'result-row'})
    #print(post_listings)
    #wartosci beda jezeli w link bedzie prawidlowy
    #post_title = post_listings[0].find(class_='result-title').text
    #post_url = post_listings[0].find('a').get('href')
    #post_price = post_listings[0].find(class_='result-price').text

    #print(post_title)
    #print(post_url)
    #print(post_price)

    final_postings = []
    for post in post_listings:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')
        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'NA'

        if post.find(class_="result-image").get('data-ids'):
            post_image_id = post.find(class_="result-image").get('data-ids').split(',')[0].split(':')[1]
            #print(post_image_url)
            post_image_url = BASE_IMAGE_URL.format(post_image_id)
            #print(post_image_url)
        else:
            post_image_url = 'https://craigslist.org/images/peace.jpg'

        final_postings.append((post_title, post_url, post_price, post_image_url))

    #prinint list of tags , prining firs element in this tag list
    #print(post_titles[0])
    #prinint just text
    #print(post_titles[0].text)
    #get link
    #print(post_titles[0].get('href'))
    #print(data)



    stuff_for_frontend = {
        'search': search,
        'final_postings': final_postings,
    }
    return render(request, 'my_app/new_search.html', stuff_for_frontend)