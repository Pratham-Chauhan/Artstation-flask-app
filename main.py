from flask import Flask, render_template, render_template_string, redirect
import requests as r
# from random import randint
import random

tdata = []
refresh = 1
img_size = 'medium'
art_urls = []

def Trending_Art_Extract(page_no):
    global refresh, art_urls, tdata
    art_urls = []

    if refresh:
        print('refresh is on'.title())
        trend_url = "https://www.artstation.com/api/v2/community/explore/projects/trending.json?page=%s&dimension=all&per_page=100"%(page_no)
        tdata = r.get(trend_url)
        if tdata.status_code == 200:
            tdata = tdata.json()['data']
            print('images fetch:', len(tdata))
            # refresh = 0
        else: 
            print("Status Code is Wrong:", tdata.status_code)
            return
        
    else:
        print('refresh is off'.title())

    
    for rn in random.sample(range(100), 30 ):
        artwork = tdata[rn]
        art_hash = artwork['hash_id']
        cover_url = artwork['smaller_square_cover_url']

        art_urls.append({'URL': cover_url, 'hash': art_hash})
        
        # print(artwork['user']['username'],'-', artwork['title'],'\n')
        # print('Hash:',art_hash) 

        # cover_url = cover_url.split('/')
        # del cover_url[ cover_url.index('smaller_square') - 1 ]
        # cover_url = '/'.join(cover_url).replace("smaller_square", img_size)


def download_art(art_hash):
    art_url = f"https://www.artstation.com/projects/{art_hash}.json"
    x2 = r.get(art_url)

    cover_art = x2.json()['cover_url']
    image_url = x2.json()['assets'][0].get('image_url')

    if cover_art==image_url:
        return [cover_art]
    return [cover_art, image_url, image_url.replace('large', '4k')]


app = Flask(__name__)

@app.route('/<int:n>')
def index(n):
    Trending_Art_Extract(n)
    return render_template('artstation_gallery.html', urls=art_urls, page=n)

@app.route('/')
def go_to_page():
    n = random.randint(1, 50)
    print(n)
    
    return redirect(f'/{n}')

@app.route('/view/<art_hash>')
def view_art(art_hash):
    return render_template("image_viewer.html", full_url = download_art(art_hash))

if __name__ == "__main__":
    app.run(host="192.168.43.55", debug=True)
    

