from flask import Flask, render_template, render_template_string, redirect, make_response, jsonify
import requests as r
# from random import randint
import random
from concurrent.futures import ThreadPoolExecutor
from threading import Thread

# chrome webdriver method
import undetected_chromedriver as uc
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import json 

# initiate Web Driver
print('Initating Driver')
DRIVER = ChromeDriverManager().install()

options = Options()
options.headless = True

driver = uc.Chrome(executable_path=DRIVER, options=options)
print('Driver Ready\n')


tdata = []
refresh = 1
img_size = 'medium'
art_urls = []

cache_urls = dict()

def cache_artURL():
    all_hsh = [j['hash'] for j in art_urls[:]]
    remaing_hsh = list(set(all_hsh) - set(cache_urls.keys()))
    print("Remaining:", len(remaing_hsh))
    print('Making Requests:\n ')
    
    with ThreadPoolExecutor() as executor:
        executor.map(download_art, remaing_hsh)


def Trending_Art_Extract(page_no):
    global refresh, art_urls, tdata
    art_urls = []

    if refresh:
        print('refresh is on'.title())
        trend_url = "https://www.artstation.com/api/v2/community/explore/projects/trending.json?page=%s&dimension=all&per_page=100" % (
            page_no)
        tdata = r.get(trend_url)
        if tdata.status_code == 200:
            tdata = tdata.json()['data']
            print('images fetch:', len(tdata))
            # refresh = 0
        else:
            print("Status Code is Wrong : ", tdata.status_code)
            return

    else:
        print('refresh is off'.title())

    # for rn in random.sample(range(100), 21):
    #     artwork = tdata[rn] #selecting art at random

    random.shuffle(tdata)
    for artwork in tdata:
        if artwork['hide_as_adult']:
            print("IT'S ADULT CONTENT: ", artwork['hash_id'])
            continue
    
        art_urls.append({'URL': artwork['smaller_square_cover_url'],
                         'hash': artwork['hash_id'],
                         'title': artwork['title'],
                         # artist
                         'artist': artwork['user']['full_name'],
                         'artist_url': artwork['user']['username'],
                         'artist_img': artwork['user']['medium_avatar_url']})

        # cover_url = cover_url.split('/')
        # del cover_url[ cover_url.index('smaller_square') - 1 ]
        # cover_url = '/'.join(cover_url).replace("smaller_square", img_size)
    print(len(art_urls))

    # Artstation site updated their security, so cannot use requests, it blocks the script completely.
    # Thread(target=cache_artURL).start()


def download_art(art_hash):
    print('>', art_hash)
    art_url = f"https://www.artstation.com/projects/{art_hash}.json"
    '''
    try:
        response = r.get(art_url)
        x2 = response.json()
    except Exception as e:
        print('status code:', response.status_code,'\nurl:', art_url,'\nerror:', e, '\n request failed!')
    ''' 
    # have to use chrome webdriver to prevent cloudflare protection
    print('using webdriver instead...')
    driver.get(art_url)

    soup = BeautifulSoup(driver.page_source, features='lxml')
    x2 = json.loads(soup.text)



    cover_art = x2['cover_url']

    image_urls = []

    for img in x2['assets']:
        print(img.get('image_url'))
        if img['has_image'] == True: image_urls.append(img.get('image_url'))
    # if cover_art == image_url:
    #     return [cover_art]

    rdata = [cover_art, *image_urls,  x2['title']] # image_url.replace('large', '4k')
    cache_urls[art_hash] = rdata
    return rdata


app = Flask(__name__)

@app.route('/<int:n>')
def index(n):
    Trending_Art_Extract(n)
    return render_template('home.html', urls=art_urls, page=n)


@app.route('/')
def go_to_page():
    n = random.randint(1, 100)
    print(n)

    return redirect(f'/{n}')


@app.route('/view/<art_hash>')
def view_art(art_hash):
    cu = cache_urls.get(art_hash)
    if cu:
        print('\nFound Cached URLs')
        return render_template("image_viewer.html", full_url=cu, hash=art_hash)
    else:
        return render_template("image_viewer.html", full_url=download_art(art_hash), hash=art_hash)


# @app.route('/load')
# def load_more():
#     res = make_response(jsonify(tdata[:10]), 200)


if __name__ == "__main__":
    app.run(debug=True)
