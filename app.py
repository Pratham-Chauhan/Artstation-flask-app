from flask import Flask, render_template, render_template_string
import requests as r
import random

tdata = []
refresh = 1
img_size = 'medium'
art_urls = []

def Trending_Art_Download():
    global refresh, art_urls, tdata
    art_urls = []
    if refresh:
        print('refresh is on'.title())
        trend_url = "https://www.artstation.com/api/v2/community/explore/projects/trending.json?page=%s&dimension=all&per_page=100"%(random.randint(1, 50))
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
   
    for rn in random.sample(range(100), 30):
        artwork = tdata[rn]
        art_hash = artwork['hash_id']
        cover_url = artwork['smaller_square_cover_url']
        art_urls.append({'URL': cover_url, 'hash': art_hash})

def download_art(art_hash):
    art_url = "https://www.artstation.com/projects/%s.json"%art_hash
    x2 = r.get(art_url)

    img_url = x2.json()['cover_url']
    return img_url


app = Flask(__name__)
@app.route('/')
def index():
    Trending_Art_Download()
    return render_template('artstation_gallery.html', urls=art_urls)

@app.route('/view/<art_hash>')
def view_art(art_hash):
    return render_template_string('<img src= "{{full_res}}">', full_res= download_art(art_hash))

if __name__ == "__main__":
    app.run()
    

