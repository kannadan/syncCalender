import urllib
import getpass
import requests
from http import cookiejar
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import json
import dryscrape
import sys
import time


def login(addr):
    username = input("giv username: ")
    password = getpass.getpass("giv password: ")

    if 'linux' in sys.platform:
    # start xvfb in case no X is running. Make sure xvfb
    # is installed, otherwise this won't work!
        dryscrape.start_xvfb()

    sess = dryscrape.Session()
    sess.set_attribute('auto_load_images', False)
    sess.visit(addr)
    name = sess.at_xpath('//*[@id="username"]')
    name.set(username)

    password2 = sess.at_xpath('//*[@id="password"]')
    password2.set(password)
    sess.render('test.png')
    print("login in")
    #name.form().submit()
    btn = sess.at_xpath('//*[@class="form-signin"]')
    btn.submit()

    sess.render('test2.png')
    print(sess.cookies())


    html = sess.driver.body()

    html = BeautifulSoup(html).prettify()
    print(html)

if __name__ == "__main__":
    url = 'https://aapo.oulu.fi/web_aapo/lukujarjestys'
    login(url)
