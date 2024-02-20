import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import asyncio
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# BBC
def total_halaman_scrapping_bbc(query):
    url = 'https://www.bbc.co.uk/search?q='+query
    # Mengirim permintaan HTTP ke server dan mendapatkan tanggapan
    response = requests.get(url)

    # Memeriksa apakah permintaan berhasil (status code 200)
    if response.status_code == 200:
        # Parsing HTML dengan BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Menemukan elemen berita terkini
        page = soup.find_all('li', class_='ssrcss-hp3otd-StyledListItem-PageButtonListItem e1ksme8n1')
        
        # mengambil nilai terakhir dari array page
        if len(page) > 0:
            return int(page[-1].text)
        else:
            return 0
    else:
        return 0

def isiKontenBBC(page):
    url = page

    # Check if the URL is valid
    if not url.startswith('http://') and not url.startswith('https://'):
        return "Invalid URL"

    # Mengirim permintaan HTTP ke server dan mendapatkan tanggapan
    response = requests.get(url)

    # Memeriksa apakah permintaan berhasil (status code 200)
    if response.status_code == 200:
        # Parsing HTML dengan BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Menemukan elemen berita terkini
        news_articles = soup.find('article', class_='ssrcss-pv1rh6-ArticleWrapper e1nh2i2l5')

        if news_articles is not None:
            return news_articles.text.strip()
        else:
            return "Konten Tidak Ditemukan"
    else:
        return "Konten Tidak Ditemukan"

def scrape_bbc(query,page):
    # URL situs web target
    url = 'https://www.bbc.co.uk/search?q='+query+'&page='+str(page)

    # Mengirim permintaan HTTP ke server dan mendapatkan tanggapan
    response = requests.get(url)

    # Memeriksa apakah permintaan berhasil (status code 200)
    if response.status_code == 200:
        # Parsing HTML dengan BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Menemukan elemen berita terkini
        news_articles = soup.find_all('li')

        # membuat array baru untuk menyimpan objek berita
        data = []
        idKonten = 0

        # Menampilkan judul dan link berita terkini
        for article in news_articles:
            headline = article.find('a', class_='ssrcss-its5xf-PromoLink exn3ah91')
            caption = article.find('p', class_='ssrcss-1q0x1qg-Paragraph e1jhz7w10')
            path = article.find('img')


            if headline and caption and path:
                # menambahkan objek berita ke dalam array data
                idKonten += 1
                data.append({
                    "id" : idKonten,
                    "judul" : headline.text.strip(),
                    "caption" : caption.text.strip(),
                    "link" : headline['href'],
                    "path" : path['src'],
                    "konten" : isiKontenBBC(headline['href'])
                })

        return data


# Kompas
def total_halaman_scrapping_kompas(query):
    url = 'https://search.kompas.com/search/?q='+query
    driver = webdriver.Chrome()

    try:
        driver.get(url)

        # Wait until the page is fully loaded and the desired element is present
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='gsc-cursor-page']"))
        )

        pages = driver.find_elements(By.XPATH, "//div[@class='gsc-cursor-page']")

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        tombolhalaman = soup.find_all('div', class_='gsc-cursor-page')

        if len(tombolhalaman) > 0:
            print(pages[-1].text)
            return int(pages[-1].text)
        return 0

    finally:
        driver.quit()

def scrapping_kompas(query, page):
    # URL situs web target
    url = 'https://search.kompas.com/search/?q='+query+'&gsc.page='+str(page)

    driver = webdriver.Chrome()

    try:
        driver.get(url)
        #  Wait until the page is fully loaded and the desired element is present
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='gsc-webResult gsc-result']"))
        )

        news_articles = driver.find_elements(By.XPATH, "//div[@class='gsc-webResult gsc-result']")
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        news_articles = soup.find_all('div', class_='gsc-webResult gsc-result')
        data = []

        for article in news_articles:
            headline = article.find('a', class_='gs-title')
            caption = article.find('div', class_='gs-bidi-start-align gs-snippet')
            path = article.find('img', class_='gs-image')

            if headline and caption and path:
                konten = isi_konten_kompas(headline['href'])

                data.append({
                    "judul" : headline.text.strip(),
                    "caption" : caption.text.strip(),
                    "link" : headline['href'],
                    "path" : path['src'],
                    "konten" : konten
                })

        return data
    finally:
        driver.quit()

def isi_konten_kompas(link):
    url = link

    try:
        # Check if the URL is valid
        if not url.startswith('http://') and not url.startswith('https://'):
            return "Invalid URL"

        # Mengirim permintaan HTTP ke server dan mendapatkan tanggapan
        response = requests.get(url)

        # Memeriksa apakah permintaan berhasil (status code 200)
        if response.status_code == 200:
            # Parsing HTML dengan BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            # Menemukan elemen berita terkini
            news_articles = soup.find('div', class_='clearfix')

            if news_articles is not None:
                karaktertidakdiperlukan = ["\n", "\t", "\r", "ADVERTISEMENT"]

                konten = news_articles.text.strip()

                for i in karaktertidakdiperlukan:
                    konten = konten.replace(i, "")

                return konten
            else:
                return "Konten Tidak Ditemukan"
        else:
            return "Konten Tidak Ditemukan"

    except Exception as e:
        return str(e)


# Tribun News
def total_halaman_tribune(query):
    url = 'https://www.tribunnews.com/search?q='+query

    driver = webdriver.Chrome()

    try:
        driver.get(url)

        # Wait until the page is fully loaded and the desired element is present
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='gsc-cursor-page']"))
        )

        pages = driver.find_elements(By.XPATH, "//div[@class='gsc-cursor-page']")

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        tombolhalaman = soup.find_all('div', class_='gsc-cursor-page')

        if len(tombolhalaman) > 0:
            print(pages[-1].text)
            return int(pages[-1].text)
        return 0

    finally:
        driver.quit()

def scrapping_tribune_two(query, page):
    url = 'https://www.tribunnews.com/search?q='+query+'&gsc.page='+str(page)

    driver = webdriver.Chrome()

    try:
        driver.get(url)
        #  Wait until the page is fully loaded and the desired element is present
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='gsc-webResult gsc-result']"))
        )

        news_articles = driver.find_elements(By.XPATH, "//div[@class='gsc-webResult gsc-result']")
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        news_articles = soup.find_all('div', class_='gsc-webResult gsc-result')
        data = []

        for article in news_articles:
            headline = article.find('a', class_='gs-title')
            caption = article.find('div', class_='gs-bidi-start-align gs-snippet')
            path = article.find('img', class_='gs-image')

            if headline and caption and path:
                konten = isiKontenTribune(headline['href'])

                data.append({
                    "judul" : headline.text.strip(),
                    "caption" : caption.text.strip(),
                    "link" : headline['href'],
                    "path" : path['src'],
                    "konten" : konten
                })

        return data

    finally:
        driver.quit()

def isiKontenTribune(link):
    url = link

    # Check if the URL is valid
    if not url.startswith('http://') and not url.startswith('https://'):
        return "Invalid URL"

    # Mengirim permintaan HTTP ke server dan mendapatkan tanggapan
    response = requests.get(url)

    # Memeriksa apakah permintaan berhasil (status code 200)
    if response.status_code == 200:
        # Parsing HTML dengan BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Menemukan elemen berita terkini
        news_articles = soup.find('div', class_='pos_rel')
        print(news_articles)

        if news_articles is not None:
            return news_articles.text.strip()
        else:
            return "Konten Tidak Ditemukan"

    else:
        return "Konten Tidak Ditemukan"


# Detik.com
def total_halaman_scrapping_detikcom(query, page):
    print(page)
    url = 'https://www.detik.com/search/searchall?query='+query+'&siteid=2&sortby=time&page='+str(page)
    # Mengirim permintaan HTTP ke server dan mendapatkan tanggapan
    response = requests.get(url)

    # Memeriksa apakah permintaan berhasil (status code 200)
    if response.status_code == 200:
        # Parsing HTML dengan BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Menemukan elemen berita terkini
        totalpage = soup.find_all('a', attrs={'dtr-act':"halaman search"})

        # fungsi rekursif untuk mendapatkan total halaman sesungguhnya apabila halaman lebih dari jumlah halaman yang ditampilkan
        if len(totalpage) > 0:
            if totalpage[-1].text.isdigit() and int(totalpage[-1].text) > 0:
                if int(totalpage[-1].text) > page:
                    return total_halaman_scrapping_detikcom(query, int(totalpage[-1].text))
                else:
                    return page
            else:
                return 0
        else:
            return page  # Mengembalikan nilai terakhir ketika halaman tidak ditemukan lagi
    else:
        return 0

def isiKontenDetikcom(page):
    url = page

    # Check if the URL is valid
    if not url.startswith('http://') and not url.startswith('https://'):
        return "Invalid URL"

    # Mengirim permintaan HTTP ke server dan mendapatkan tanggapan
    response = requests.get(url)

    # Memeriksa apakah permintaan berhasil (status code 200)
    if response.status_code == 200:
        # Parsing HTML dengan BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Menemukan elemen berita terkini
        news_articles = soup.find('div', class_='detail__body-text')

        if news_articles is not None:
            for i in news_articles.find_all('div', class_='clearfix'):
                i.decompose()
            
            for i in news_articles.find_all('style'):
                i.decompose()

            for i in news_articles.find_all('div', class_='detail__body-tag mgt-16'):
                i.decompose()

            return news_articles.text.strip()
        else:
            return "Konten Tidak Ditemukan"
    else:
        return "Konten Tidak Ditemukan"
            
def scrapping_detikcom(query, page):
    url = 'https://www.detik.com/search/searchall?query='+query+'&siteid=2&sortby=time&page='+str(page)
    # Mengirim permintaan HTTP ke server dan mendapatkan tanggapan
    response = requests.get(url)

    # Memeriksa apakah permintaan berhasil (status code 200)
    if response.status_code == 200:
        # Parsing HTML dengan BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Menemukan elemen berita terkini
        news_articles = soup.find_all('article')
        page = soup.find_all('a', attrs={'dtr-act':"halaman search"})


        if len(news_articles) == 0:
            return {
                "status" : "error",
                "status_code" : 404,
                "message" : "Data Tidak Ditemukan"
            }

        data = []
        idKonten = 0

        # Menampilkan judul dan link berita terkini
        for article in news_articles:
            headline = article.find('a')
            judul = article.find('h2', class_='title')
            caption = article.find('p')
            path = article.find('img')
            tanggal = article.find('span', class_='date')
            # link = article.find('a', class_='gs-c-promo-heading')

            if headline and caption and path and judul and tanggal:
                for tanggalonly in tanggal.find_all('span', class_='category'):
                    tanggalonly.decompose()

                idKonten += 1

                data.append({
                    "id" : idKonten,
                    "judul" : judul.text.strip(),
                    "caption" : caption.text.strip(),
                    "link" : headline['href'],
                    "path" : path['src'],
                    "tanggal": tanggal.text.strip(),
                    "konten" : isiKontenDetikcom(headline['href'])                 
                })
        
        return data


# Liputan6
def scrapping_liputanenam(query):
    url = "https://www.liputan6.com/search?q="+query
    driver = webdriver.Chrome()  # Anda perlu memiliki ChromeDriver diinstal

    try:
        driver.get(url)
        time.sleep(5)  # Tunggu hingga halaman sepenuhnya dimuat

        data = []

        while True:
            # Hitung tinggi halaman sebelum melakukan scroll
            previous_height = driver.execute_script("return document.body.scrollHeight")

            # Scroll ke bawah
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)

            # Tunggu hingga halaman sepenuhnya dimuat
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//article[@class='articles--iridescent-list--item articles--iridescent-list--text-item']"))
            )
            
            news_articles = driver.find_elements(By.XPATH, "//article[@class='articles--iridescent-list--item articles--iridescent-list--text-item']")

            soup = BeautifulSoup(driver.page_source, 'html.parser')

            news_articles = soup.find_all('article', class_='articles--iridescent-list--item articles--iridescent-list--text-item')

            # membuat array baru untuk menyimpan objek berita
            
            for article in news_articles:
                headline = article.find('a', class_='ui--a articles--iridescent-list--text-item__title-link')
                caption = article.find('div', class_='articles--iridescent-list--text-item__summary articles--iridescent-list--text-item__summary-seo')
                path = article.find('img')
                # link = article.find('a')

                if headline and caption and path and link:
                    # konten = isiKontenLiputanenam(link['href'])

                    data.append({
                        "judul" : headline.text.strip(),
                        "caption" : caption.text.strip(),
                        "link" : headline['href'],
                        "path" : path['src'],
                        # "konten" : konten
                    })

            # Hitung tinggi halaman setelah melakukan scroll
            new_height = driver.execute_script("return document.body.scrollHeight")

            # Jika tinggi halaman tidak berubah setelah melakukan scroll, maka proses scroll selesai
            if new_height == previous_height:
                break

        return data

    finally:
        driver.quit()


# CNN Indonesia
def total_halaman_cnn_indonesia(query):
    url = 'https://www.cnnindonesia.com/search/?query=' + query

    driver = webdriver.Chrome()  # You need to have ChromeDriver installed

    try:
        driver.get(url)

        # Wait until the page is fully loaded and the desired element is present
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[@dtr-evt='halaman']"))
        )

        pages = driver.find_elements(By.XPATH, "//a[@dtr-evt='halaman']")
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        page = soup.find_all('a', attrs={'dtr-evt':"halaman"})
        print(page)

        if len(page) > 0:
            return int(page[-2].text)
        else:
            return 0

    finally:
        driver.quit()

def scrapping_cnn_indonesia(query, page):
    url = 'https://www.cnnindonesia.com/search/?query='+query+'&page='+str(page)
    # Mengirim permintaan HTTP ke server dan mendapatkan tanggapan
    response = requests.get(url)

    # Memeriksa apakah permintaan berhasil (status code 200)
    if response.status_code == 200:
        # Parsing HTML dengan BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Menemukan elemen berita terkini
        news_articles = soup.find_all('article', class_='flex-grow')
        
        # membuat array baru untuk menyimpan objek berita
        data = []

        for article in news_articles:
            headline = article.find('h2')
            img_path = article.find('img')
            link = article.find('a')

            if headline and img_path and link:
                konten = isi_konten_cnn_indonesia(link['href'])

                data.append({
                    "judul" : headline.text.strip(),
                    "link" : link['href'],
                    "path" : img_path['src'],
                    "konten" : konten
                })
                
        return data

def isi_konten_cnn_indonesia(link):
    url = link

    try:
        # Check if the URL is valid
        if not url.startswith('http://') and not url.startswith('https://'):
            return "Invalid URL"

        # Mengirim permintaan HTTP ke server dan mendapatkan tanggapan
        response = requests.get(url)

            # Memeriksa apakah permintaan berhasil (status code 200)
        if response.status_code == 200:
            # Parsing HTML dengan BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            # Menemukan elemen berita terkini
            news_articles = soup.find('div', class_='detail-text text-cnn_black text-sm grow min-w-0')

            if news_articles is not None:
                karaktertidakdiperlukan = ["\n", "\t", "\r", "ADVERTISEMENT", "SCROLL TO CONTINUE WITH CONTENT"]

                konten = news_articles.text.strip()

                for i in karaktertidakdiperlukan:
                    konten = konten.replace(i, "")

                return konten
            else:
                return "Konten Tidak Ditemukan"
        else:
            return "Konten Tidak Ditemukan"

    except Exception as e:
        return str(e)
