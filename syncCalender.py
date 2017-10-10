import urllib
import getpass
import requests
from http import cookiejar
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import json

def login(addr):
    username = input("giv username: ")
    password = getpass.getpass("giv password: ")
    posti = "https://aapo.oulu.fi/Shibboleth.sso/SAML2/POST"
    ua = UserAgent()
    session = requests.session()
    response = session.get(addr)
    cookies = session.cookies.get_dict()
    print(cookies)
    cookie = cookies["JSESSIONID"]
    values = {'j_username' : username,
            "_eventId_proceed" : "",
          'j_password' : password }

    headers = {"Host" : "login.oulu.fi",
                "User-Agent" : ua.random,
                "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language" : "fi-FI,fi;q=0.8,en-US;q=0.5,en;q=0.3",
                "Accept-Encoding" : "gzip, deflate, br",
                "Referer" : response.url,
                "Content-Type" : "application/x-www-form-urlencoded",
                "Content-Length" : "46",
                "Cookie" : "JSESSIONID=" + cookie,
                "Connection" : "keep-alive",
                "Upgrade-Insecure-Requests" : "1"}



    SAML_url = response.url
    response = session.post(SAML_url, data=values, headers=headers)
    print(response.headers)
    print("\n")
    print(session.cookies.get_dict())
    print("\n")
    #print(response.text)
    soup = BeautifulSoup(response.text)
    #print(soup.prettify())

    payload = {"RelayState" : addr,
                "SAMLResponse" : soup.find("input", {"name":"SAMLResponse"})["value"]}
    resp2 = session.post(posti, data=payload, headers=session.headers )
    print(resp2.text)


if __name__ == "__main__":
    url = 'https://aapo.oulu.fi/web_aapo/lukujarjestys'
    login(url)
