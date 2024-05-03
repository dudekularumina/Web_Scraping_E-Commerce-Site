from bs4 import BeautifulSoup
import requests

url="https://www.amazon.in/s?k=cameras+for+photography&crid=NSKHN12UPGQ4&sprefix=cameras+for+%2Caps%2C214&ref=nb_sb_ss_ts-doa-p_2_12"
response=requests.get(url)
print(response.status_code)


# soup=BeautifulSoup(" ")
# print(soup.prettify())