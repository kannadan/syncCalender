import urllib
import getpass
import requests
from http import cookiejar
from bs4 import BeautifulSoup

url = 'https://aapo.oulu.fi/web_aapo/lukujarjestys'
username = input("giv username: ")
password = getpass.getpass("giv password: ")

values = {'j_username' : username,
            "_eventId_proceed" : "",
          'j_password' : password }
print(values)

session = requests.session()

response = session.get(url)
cookies = session.cookies.get_dict()
print (cookies)

SAML_url = response.url
response = session.post(SAML_url, payload)
