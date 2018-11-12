import requests
from bs4 import BeautifulSoup

session = requests.session()
startURL = "https://www.fullhdfilmizleten.org/"
home_page_header = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
}
resp = session.post(startURL, headers=home_page_header)
category_html = BeautifulSoup(resp.content, 'html.parser')

for cat in category_html.select('div.sayfa-sag > div#sag-kategori-tablo'):
    for category in cat.select('div.kategoriler.ust > ul.ek-liste > li > h4 > a '):
        category_name = category.get_text(strip=True)
        category_link = category.attrs['href']

        category_movie_url = "https://www.fullhdfilmizleten.org/{}".format(category_link)
        category_movie_header = {
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
        category_movie_resp = session.post(category_movie_url, headers=category_movie_header)
        movie_ex = BeautifulSoup(category_movie_resp.content, 'html.parser')
        movie_list = []

        for movie_info in movie_ex.select('div.sayfa-sol > div#icerik > div.film-k.kutu-icerik.kat'):
            m_url = movie_info.select_one('div.play.fa.fa-play-circle > h5 > a').attrs['href']
            quality = movie_info.select_one('div.kalite').get_text(strip=True)
            img_src = movie_info.select_one('div.resim > img').attrs['src']
            img = "https://www.fullhdfilmizleten.org{}".format(img_src)
            imdb = movie_info.select_one('div.imdb > b').get_text(strip=True)
            type = movie_info.select_one('div.bilgi.gizle > ul.ek > li.tur').get_text(strip=True)
            movie_description = movie_info.select_one('div.bilgi.gizle > div.aciklama').get_text(strip=True)
            vision_date = movie_info.select('div.bilgi.gizle > ul.ek > li.a')[1].get_text(strip=True)
            time = movie_info.select('div.bilgi.gizle > ul.ek > li')[4].get_text(strip=True)


            movie_url = "https://www.fullhdfilmizleten.org{}".format(m_url)
            movie_header = {
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}

            movie_resp = session.post(movie_url, headers=movie_header)
            movie_data = BeautifulSoup(movie_resp.content, 'html.parser')

            for movies in movie_data.select('div#sayfa > div#sayfa-ic > div#film-tab'):
                try:
                    movie_path = movies.select('div.tab-cizgi > ul.tab-baslik.dropit > li.dropit-trigger > ul.dropit-submenu > li > a')[0].attrs['href']
                except:
                    continue

                movie_origin_url = "https://www.fullhdfilmizleten.org{}".format(movie_path)
                movie_origin_header = {"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
                movie_origin_resp = session.post(movie_origin_url, headers=movie_origin_header)

                movie_orgin_data = BeautifulSoup(movie_origin_resp.content, 'html.parser')

                for movie_orgin in movie_orgin_data.select('div#sayfa > div#sayfa-ic'):
                    try:
                        movie_orgin_path = movie_orgin.select('div#film-tab > div.tab-dis > div.tab-icerik > iframe')[0].attrs['src']
                        movie_name = movie_orgin.select('div.izle-ust > div.resim-bg.test > div.resim-bg-ic > div.slayt-tablo > div.slayt-orta > h1 > a')[1].get_text(strip=True)

                        movie_list.append({
                            'category': category_name,
                            'movie_name': movie_name,
                            'movie_path': movie_orgin_path,
                            'movie_description': movie_description,
                            'image': img,
                            'movie_type': type.split(':')[- 1],
                            'movie_time': time.split(':')[- 1],
                            'vision_date': vision_date.split(':')[- 1],
                            'quality': quality,
                            'imdb': float(imdb)

                        })
                    except:
                        continue
        if category_name == "+18 Erotik" or category_name == "4K UHD":
            continue
        movie_doc = {
            'movies': movie_list
        }
        # print(movie_doc)
        falcon_resp = requests.post("http://127.0.0.1:8000/data", json=movie_doc)
        print(falcon_resp.status_code)