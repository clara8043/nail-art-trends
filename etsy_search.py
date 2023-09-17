
import requests

URL = "https://www.etsy.com/ca/market/nails?ref=pagination&page=1"
page = requests.get(URL)

print(page.text)