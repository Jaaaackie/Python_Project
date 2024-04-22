import requests
from bs4 import BeautifulSoup

def create_soup(url):
    res = requests.get(url)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, 'lxml')
    return soup

def print_news(index, title, link):
    print("{}. {}".format(index + 1, title))
    print(  "(Link : {})".format(link))

def scrape_weather():
    print('[Wetter heute]')

    url = 'https://weather.com/de-DE/weather/today/l/57cc6eb02c4a08a4b126b05ffd2f41db82b40e54868394e6087105b9f5d4d83d'
    soup = create_soup(url)
    
    location = soup.find("h1", attrs = {"class": "CurrentConditions--location--1YWj_"}).get_text()
    crt_timestamp = soup.find("span", attrs = {"class": "CurrentConditions--timestamp--1ybTk"}).get_text().replace("Stand", "stand")

    # jetztige Temperatur
    crt_temp = soup.find("span", attrs = {"class": "CurrentConditions--tempValue--MHmYY"}).get_text()

    # Tagsüber/Nacht
    cast = soup.find("div", attrs = {"class": "CurrentConditions--tempHiLoValue--3T1DG"}).get_text()

    # Warnung
    warning = soup.find("h2", attrs = {"class": "AlertHeadline--alertText--38xov"}).get_text().replace("Warnung vor", "")
    
    # Ausgabe
    print("Wetterbericht in {}, die aktuelle Uhrzeit {}".format(location, crt_timestamp))
    print("Jetzt {} ({})".format(crt_temp, cast))
    print()
    print("Warnung vor{}".format(warning))
    print()

#######################################################
# [Top 2 Nachrichten heute]
# 1. Titel
# (Link : https://...)

# 2. Titel
# (Link : https://...)

def scrape_top_news():
    print("[Top 2 Nachrichten heute]")
    url = 'https://news.google.com/home?hl=de&gl=DE&ceid=DE:de'
    soup = create_soup(url)
    news_list = soup.find_all("div", attrs = {"class": "afJ4ge"})[0].find_all("article", attrs = {"class": "IBr9hb"})

    for index, news in enumerate(news_list): # enumerate() verwenden, um Index zu zeigen
        title = news.find("a", attrs = {"class": "gPFEn"}).get_text()
        link = news.find("a")["href"].replace("./", "https://news.google.com/")

        print_news(index, title, link)

    print()

#######################################################
# [Wisschenschaft & Technik Nachrichten]
# 1. Titel
# (Link : https://...)

# 2. Titel
# (Link : https://...)

# 3. Titel
# (Link : https://...)
    
def scrape_it_news():
    print("[Wissenschaft & Technik]")
    url = 'https://news.google.com/topics/CAAqKAgKIiJDQkFTRXdvSkwyMHZNR1ptZHpWbUVnSmtaUm9DUkVVb0FBUAE?hl=de&gl=DE&ceid=DE%3Ade'
    soup = create_soup(url)
    news_list = soup.find_all("c-wiz", attrs = {"class": "PO9Zff Ccj79 kUVvS"}, limit = 3)
    
    for index, news in enumerate(news_list):
        # Gibt es ein Bild im Titel?
        # a_index = 0
        # img = news.find("img")
        # if img:
        #     a_index = 1 # Wenn es ein img-Tag gibt, verwende die Info des ersten a-Tag

        # a_tag = news.find_all("a")[a_index]
        # title = a_tag.get_text()
        # link = a_tag["href"]
        title = news.find("a", attrs = {"class": "gPFEn"}).get_text()
        link = news.find("a")["href"].replace("./", "https://news.google.com/")
        print_news(index, title, link)
    
    print()

if __name__ == '__main__':
    scrape_weather() # Wetterinformation
    scrape_top_news() # Top 2 Nachrichten
    scrape_it_news() # IT-Nachrichten
