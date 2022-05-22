import requests
from requests.compat import quote_plus
from django.shortcuts import render
from bs4 import BeautifulSoup
from . import models
# Create your views here.

BASE_CRAIGSLIST_URL = 'https://losangeles.craigslist.org/search/bbb?query={}'

BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'

def home(request):
    return render(request, 'layout.html')


def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)

    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search))
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')

    post_listings = soup.findAll('li', {'class': 'result-row'})

    final_postings = []

    for post in post_listings:
        post_title = post.find('a', {'class': 'result-title'}).text
        post_url = post.find('a', {'class': 'result-title'}).get('href')

        if  post.find(class_="result-image").get('data-ids'):
            post_img_id = post.find(class_="result-image").get('data-ids').split(',')[0].split(':')[1]

            post_img_url = BASE_IMAGE_URL.format(post_img_id)
        else:
            post_img = 'N/A'
            post_img_url = 'https://via.placeholder.com/300?text=No+Image+Found'

        final_postings.append({
            'post_title': post_title,
            'post_url': post_url,
            'post_img_url': post_img_url,
        })

    context = {
        'search': search,
        'final_postings': final_postings,
    }

    return render(request, 'new_search.html', context)
