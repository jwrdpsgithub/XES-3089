import requests
from bs4 import BeautifulSoup, NavigableString, Tag

def get_random_xkcd_url() -> str:
    response = requests.get("https://c.xkcd.com/random/comic")
    soup = BeautifulSoup(response.content, 'html.parser')

    comic_div = soup.find('div', attrs={"id": "comic"})

    if comic_div:
        img_tag = comic_div.find('img')

    if img_tag and 'src' in img_tag.attrs:
        return img_tag['src']
    
    return ""

def get_img_from_url(url: str, path: str):
    image_response = requests.get(url)
    open(path, 'wb').write(image_response.content)

def get_alt_text_from_xkcd_url(url: str):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    comic_div = soup.find('div', attrs={"id": "comic"})

    if comic_div:
        img_tag = comic_div.find('img')
    else:
        return "NO"

    if img_tag and 'title' in img_tag.attrs:
        return img_tag['title']

def download_random_xkcd(path: str):
    img_url = f"https:{get_random_xkcd_url()}"
    get_img_from_url(img_url, path)
