from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from requests.compat import quote_plus
from . import models


BASE_CRAIGSLIST_URL = 'https://warsaw.craigslist.org/search/jjj?query={}'

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
    soup = BeautifulSoup(data, features='html.parser')
    post_titles = soup.find_all('a', {'class': 'result-title'})
    #prinint list of tags , prining firs element in this tag list
    #print(post_titles[0])
    #prinint just text
    print(post_titles[0].text)
    #get link
    print(post_titles[0].get('href'))
    #print(data)
    stuff_for_frontend = {
        'search': search,
    }
    return render(request, 'my_app/new_search.html', stuff_for_frontend)

    #9:13