from pyvirtualdisplay import Display
from selenium import webdriver
import getpass
from selenium.webdriver.common.keys import Keys
import time


def login(addr):
    username = input("giv username: ")
    password = getpass.getpass("giv password: ")


    display = Display(visible=1, size=(800, 600))
    display.start()

    browser = webdriver.Firefox()
    browser.get(addr)
    print(browser.title)
    name = browser.find_element_by_id("username")
    passs = browser.find_element_by_id("password")
    name.send_keys(username)
    passs.send_keys(password)
    passs.send_keys(Keys.RETURN)
    time.sleep(10)
    events = browser.find_elements_by_css_selector("div.rbc-event-content")
    for elem in events:
        print (elem.text)

#    browser.quit()
    #display.stop()


if __name__ == "__main__":
    url = 'https://aapo.oulu.fi/web_aapo/lukujarjestys'
    login(url)
