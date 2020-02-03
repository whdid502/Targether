import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsteam

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
r = requests.get('https://store.steampowered.com/search/?specials=1&filter=topsellers', headers = headers)

soup = BeautifulSoup(r.text, 'html.parser')
games = soup.select('div#search_resultsRows > a')

for game in games:
    game_link = game['href']
    game_img = game.select_one('div.search_capsule > img').get('src')
    game_title = game.select_one('div.responsive_search_name_combined >  div.col.search_name.ellipsis > span').text
    game_original_pirce = game.select_one('div.responsive_search_name_combined > div.col.search_price_discount_combined.responsive_secondrow > div.col.search_price.discounted.responsive_secondrow > span > strike').text
    game_discount_rate = game.select_one('div.responsive_search_name_combined > div.col.search_price_discount_combined.responsive_secondrow > div.col.search_discount.responsive_secondrow > span').text
    combined_price = game.select_one('div.responsive_search_name_combined > div.col.search_price_discount_combined.responsive_secondrow > div.col.search_price.discounted.responsive_secondrow')
    unwanted_price = combined_price.find('span')
    unwanted_price.extract()
    print(game_link)