import urllib
import getpass
from http import cookiejar
from bs4 import BeautifulSoup

url = 'https://aapo.oulu.fi/web_aapo'
username = input("giv username: ")
password = getpass.getpass("giv password: ")

values = {'username' : username,
          'password' : password }
print(values)

data = urllib.parse.urlencode(values)
cookies = cookiejar.CookieJar()
"""
opener = urllib.request.build_opener(
    urllib.request.HTTPRedirectHandler(),
    urllib.request.HTTPHandler(debuglevel=0),
    urllib.request.HTTPSHandler(debuglevel=0),
    urllib.request.HTTPCookieProcessor(cookies))

response = opener.open(url, data)
the_page = response.read()
http_headers = response.info()
"""
