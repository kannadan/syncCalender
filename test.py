import dryscrape

search_keyword = 'dryscrape'

# set up a web scraping session
session = dryscrape.Session(base_url = 'http://avi.im/stuff/js-or-no-js.html')

# we don't need images
session.set_attribute('auto_load_images', False)

# visit homepage and search for a term
session.visit('/')
q = session.at_xpath('//*[@name="q"]')
q.set(search_keyword)
session.render('google.png')
q.form().submit()

# extract all links
"""for link in session.xpath('//a[@href]'):
  print (link['href'])"""

# save a screenshot of the web page
print("Screenshot written to 'google.png'")
session.set_cookie({"test=jawoifjjfwai"})
print(session.cookies())
