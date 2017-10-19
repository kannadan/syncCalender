from __future__ import print_function
from pyvirtualdisplay import Display
from selenium import webdriver
import getpass
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
from datetime import date, timedelta, datetime
from datetime import time as time2


from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import httplib2
import os


try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'       #GET YOUR OWN FROM https://developers.google.com/google-apps/calendar/quickstart/python
APPLICATION_NAME = 'Google Calendar API Python Quickstart'

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    #Didn't touch. works fine as is
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def login(addr, username, password):

    #Login function for aapo.oulu.fi/web_aapo/lukujarjestys
    #Note that while the address is a parameter for the function, this will fail on any other address
    display = Display(visible=0, size=(800, 600))
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

def makeCalender(driver, week):
    #Reads aapo calender and returns an events list
    now = datetime.now()    #gives us a year for the date object. Need to add check for end of the year!!!
    html = driver.page_source
    html = BeautifulSoup(html, "lxml")

    days = html.findAll("div", {"class":"rbc-day-slot rbc-time-column"})    #every week day
    days.extend(html.findAll("div",{"class":"rbc-day-slot rbc-time-column rbc-weekend"})) #weekend for some reason
    dates = html.find("div", {"class":"rbc-toolbar-label"}).getText()  #start date and month from calender

    start = dates.split(",")[1].split("-")[0] #get date from string: Viikko   43, 23.10. - 29.10.
    startD, startM = map(lambda x : int(x), start.strip().strip(".").split("."))

    if now.month == 1 and startM == 12: #handles days around new year
        dateS = date(now.year-1, startM, startD)
    else:
        dateS = date(now.year, startM, startD)

    allEvents = []

    for i in range(week): #sets how many weeks worth of data we collect
        for pointer, day in enumerate(days):
            events = day.findAll("div", {"class":"rbc-event"})
            for event in events:
                labelL = event.find("div", {"class":"rbc-event-label-left"}).getText() #time
                labelR = event.find("div", {"class":"rbc-event-label-right"}).getText() #class room
                content = event.find("div", {"class":"rbc-event-content"}).getText()    #course

                start, end = labelL.split("-")
                hourS, minS = map(lambda x : int(x), start.strip().split(":"))  #turns start and endtimes to ints
                hourE, minE = map(lambda x : int(x), end.strip().split(":"))

                start = datetime.combine(dateS + timedelta(pointer), time2(hourS, minS))
                end = datetime.combine(dateS + timedelta(pointer), time2(hourE, minE))

                dict = {}   #ends as json for google api
                dict["summary"] = content
                dict["location"] = labelR
                dict["start"] = {"dateTime" : start.strftime("%Y-%m-%dT%H:%M:%S"),
                                    'timeZone': 'Europe/Helsinki'}
                dict["end"] = {"dateTime" : end.strftime("%Y-%m-%dT%H:%M:%S"),
                                    'timeZone': 'Europe/Helsinki'}
                dict["reminders"] = {"useDefault": False,       #set to True and get notification 30 min in advance
                                    "overrides" : []}
                allEvents.append(dict)
                print("event found on " + start.strftime("%d.%m.%Y"))
                print("kello: " + labelL + " - Luokka: " + labelR)
                print(content + "\n")

        print("Moving to next week")
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
    return allEvents

def googlify(stuff):
    #send events to google calenders
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    for event in stuff:
        event = service.events().insert(calendarId='primary', body=event).execute()
        print ('Event created: \n%s\n' % (event.get('htmlLink')))

if __name__ == "__main__":
    username = input("giv username: ")
    password = getpass.getpass("giv password: ")
    weeks = input("give number of weeks you wanna read: ")
    url = 'https://aapo.oulu.fi/web_aapo/lukujarjestys'
    if weeks.isdigit():
        browser, display = login(url, username, password)
        if browser.title != "Aapo":
            print("Wrong username or password")
        else:
            events = makeCalender(browser, int(weeks))
            browser.quit()
            display.stop()
            print("Done with aapo, moving to google")
            googlify(events)
            print("All done. Shutting down")
    else:
        print("I need an actual number for week")
