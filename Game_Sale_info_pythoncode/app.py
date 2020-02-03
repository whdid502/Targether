from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup
app = Flask(__name__)

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/game_sale')
def game_main_page():
   return render_template('game_sales.html')

@app.route('/page_steam')
def game_steam_page():
   return render_template('steam_page.html')

@app.route('/steam_info', methods=['GET'])
def get_steam_sale():
  client = MongoClient('localhost', 27017)
  db = client.dbstemainfo
  output = []
  for s in db.sale.find():
    output.append({'steam_link' : s['steam_link'], 'steam_img': s['steam_img'], 'steam_title' : s['steam_title'], 'steam_original_price' : s['steam_original_price'], 'steam_discount_rate' : s['steam_discount_rate'] , 'steam_discount_price' : s['steam_discount_price']})
  return jsonify({'result' : output})

@app.route('/steam_info', methods=['POST'])
def steam_sale():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
    r = requests.get('https://store.steampowered.com/search/?specials=1&filter=topsellers', headers=headers)
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
        client = MongoClient('localhost', 27017)
        db = client.dbsteaminfo
        db.info.delete_many({}) # db를 초기화 하기 위한 삭제입니다.
        doc = {
            'steam_link' : game_link,
            'steam_img' : game_img,
            'steam_title' : game_title,
            'steam_original_price': game_original_pirce,
            'steam_discount_rate' : game_discount_rate,
            'steam_discount_price' : combined_price.text
        }
        db.info.insert_one(doc)
        return jsonify({'result': 'success'})

        # for s in db.info.find(): # get을 섞었습니다
        #     get_steam_info = []
        #     get_steam_info.append({'steam_link' : s['steam_link'], 'steam_img': s['steam_img'], 'steam_title': s['steam_title'], 'steam_original_price': s['steam_original_price'], 'steam_discount_rate': s['steam_discount_rate'], 'steam_discount_price': s['steam_discount_price']})
        # return jsonify({'result':'success', 'msg': '성공적으로 저장됐습니다.', 'output': get_steam_info})




if __name__ == '__main__':
   app.run('0,0,0,0',port=5000,debug=True)