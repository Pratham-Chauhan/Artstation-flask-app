from flask import Flask, render_template, render_template_string, redirect, make_response, jsonify
import requests as r
# from random import randint
import random
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
import re 


tdata = []
refresh = 1
img_size = 'medium'
art_urls = []

cache_urls = dict()

def cache_artURL():
    all_hsh = [j['hash'] for j in art_urls[:]]
    remaing_hsh = list(set(all_hsh) - set(cache_urls.keys()))
    print("Remaining:", len(remaing_hsh))

    with ThreadPoolExecutor() as executor:
        executor.map(download_art, remaing_hsh)


def Trending_Art_Extract(page_no: int):
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

    Thread(target=cache_artURL).start()


def download_art(art_hash: str) -> dict:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
    }
    print('making requests:', art_hash)
    art_url = f"https://www.artstation.com/projects/{art_hash}.json"
    x2 = r.get(art_url, headers=headers)
    print((x2, art_url))
    if x2.status_code != 200:
        print('Failed to make request.')
        return ['', '', '', '']
    
    x2 = x2.json()

    
    image_url = x2['assets'][0].get('image_url')

    links = {
        'Title': x2['title'],
        'Cover Art': x2['cover_url'],
        'Image Links': [], 
        'Video Links': []
        }   
    
    for i in x2['assets']:
        if i['has_embedded_player']:
            vid_link = re.findall(r"src='([^']*)'", i['player_embedded'])
            if vid_link:
                links['Video Links'].append(vid_link)

        else: 
            links['Image Links'].append(i['image_url'])
    
    # if cover_art == image_url:
    #     return [cover_art]

    # rdata = [cover_art, image_url, image_url.replace('/large/', '/4k/'), x2['title']]
    cache_urls[art_hash] = links
    return links


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
def view_art(art_hash: str):
    cu:dict = cache_urls.get(art_hash)
    if cu:
        print('\nFound Cached URLs')
        return render_template("image_viewer.html", full_url=cu, hash=art_hash)
    else:
        return render_template("image_viewer.html", full_url=download_art(art_hash), hash=art_hash)


if __name__ == "__main__":
    app.run(debug=True)
    # app.run(debug=True)
