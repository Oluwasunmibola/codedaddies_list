from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from urllib.parse import quote_plus
from . import models


BASE_OODLE_URL = 'https://www.oodle.com/browse/?q={}'

# Create your views here.


def home(request):
    return render(request, 'base.html')


def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    # print(quote_plus(search))
    final_url = BASE_OODLE_URL.format(quote_plus(search))
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')
    post_listings = soup.find_all('li', {'class': 'has-thumbnail'})
    # post_image = post_listings[0].find('img').get('src')
    # print(post_image)
    """
    post_title = post_listings[0].find(class_='title-link').text
    post_url = post_listings[0].find('a').get('href')
    post_price = post_listings[0].find(class_='price').text
    """

    final_postings = []
    for post in post_listings:
        post_title = post.find(class_='title-link').text
        post_url = post.find('a').get('href')
        if post.find('img').get('data-url'):
            post_image = post.find('img').get('data-url')
        else:
            post_image = post.find('img').get('src')

        post_image_alt = post.find('img').get('alt')
        if post.find(class_='price'):
            post_price = post.find(class_='price').text
        else:
            post_price = 'N/A'

        final_postings.append((post_title, post_url, post_price, post_image, post_image_alt))

    # print(final_postings)
    # print(data)
    stuff_for_frontend = {
        'search': search,
        'final_postings': final_postings,
    }
    return render(request, 'my_app/new_search.html', stuff_for_frontend)
