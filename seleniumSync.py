from pyvirtualdisplay import Display
from selenium import webdriver
import getpass
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
from datetime import date, timedelta, datetime


def login(addr, username, password):

    #Login function for aapo.oulu.fi/web_aapo/lukujarjestys
    #Note that while the address is a parameter for the function, this will fail on any other address
    display = Display(visible=1, size=(800, 600))
    display.start()

    browser = webdriver.Firefox()
    browser.get(addr)

    name = browser.find_element_by_id("username")
    passs = browser.find_element_by_id("password")
    name.send_keys(username)
    passs.send_keys(password)
    passs.send_keys(Keys.RETURN)
    time.sleep(10)  #Generous wait time for browser to load everything
    return browser, display

def makeCalender(driver):
    #Reads aapo calender and returns an events list
    now = datetime.now()    #gives us a year for the date object. Need to add check for end of the year!!!
    html = driver.page_source
    html = BeautifulSoup(html, "lxml")

    days = html.findAll("div", {"class":"rbc-day-slot rbc-time-column"})    #every week day
    days.extend(html.findAll("div",{"class":"rbc-day-slot rbc-time-column rbc-weekend"})) #weekend for some reason
    dates = html.find("div", {"class":"rbc-toolbar-label"}).getText()  #start date and month from calender

    start, end = dates.split(",")[1].split("-") #get date from string: Viikko   43, 23.10. - 29.10.
    startD, startM = map(lambda x : int(x), start.strip().strip(".").split("."))
    dateS = date(now.year, startM, startD)

    for i in range(2): #sets how many weeks worth of data we collect
        for pointer, day in enumerate(days):
            paiva = (dateS + timedelta(pointer)).isoformat()
            events = day.findAll("div", {"class":"rbc-event"})
            print(paiva)
            for event in events:
                labelL = event.find("div", {"class":"rbc-event-label-left"}).getText() #time
                labelR = event.find("div", {"class":"rbc-event-label-right"}).getText() #class room
                content = event.find("div", {"class":"rbc-event-content"}).getText()    #course
                print("kello: " + labelL + " - Luokka: " + labelR)
                print(content + "\n")


        #print("Days found " + str(len(days)))
        button = driver.find_element_by_xpath("//button[contains(.,'Seuraava')]").click() #why does it have to be regexp
        time.sleep(10)  #again sleepy times to wait for page to load
        html = driver.page_source
        html = BeautifulSoup(html, "lxml")
        days = html.findAll("div", {"class":"rbc-day-slot rbc-time-column"})
        days.extend(html.findAll("div",{"class":"rbc-day-slot rbc-time-column rbc-weekend"}))
        dateS = dateS + timedelta(7)    #adds 7 days to get to monday of next week

        #need to return a list or a class or something that has info on all of the events.
        #will get back on this once google calenders required format is known

def googlify(stuff):
    #send events to google calenders
    pass

if __name__ == "__main__":
    username = input("giv username: ")
    password = getpass.getpass("giv password: ")
    url = 'https://aapo.oulu.fi/web_aapo/lukujarjestys'
    browser, display = login(url, username, password)
    if browser.title != "Aapo":
        print("Wrong username or password")
    else:
        makeCalender(browser)
        input("just waiting around ")
    browser.quit()
    display.stop()
