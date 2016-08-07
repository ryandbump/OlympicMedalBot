import praw
import time
import requests
from bs4 import BeautifulSoup


UA = 'USA Olympics Medal Counter. Contact me at /u/theDauntingGoat'

r = praw.Reddit(UA)
r.login()


def check_condition(s):
    medals = ['gold', 'silver', 'bronze', 'medal']
    keys = ['usa', 'america', 'american', 'united states']
    title = s.title.lower()
    if any(string in title for string in medals) and any(string in title for string in keys):
        return True

def bot_action(s):
    repliedTo.append(s.id)
    writeIdToFile(s.id)
    page = requests.get('http://www.cbssports.com/olympics/news/2016-rio-olympics-medal-tracker/')
    soup = BeautifulSoup(page.content, 'html.parser')

    rows = soup.find_all('tr')
    medals = []
    header = None
    for row in rows:
        array = row.get_text().split()
        if 'Country' in array:
            header = array
        else:
            medals.append(array)

    reply_text = "##USA wins another medal!  \n  Here is the current medal standings  \n\n  " + " | ".join(header) + "  \n  :----: | :----: | :----: | :-----: | :----:  \n  "

    for entry in medals:
        if 'USA' in entry:
            boldEntry = []
            for word in entry:
                boldEntry.append("**" + word + "**")
            reply_text += " | ".join(boldEntry) + "  \n  "
        else:
            reply_text += " | ".join(entry) + "  \n  "


    s.add_comment(reply_text)
    time.sleep(1800)

def getStoredPostIds():
    storedPostsFile = open("posts.txt", "r")
    storedPosts = storedPostsFile.read()

    storedArray = storedPosts.split("\n")

    storedPostsFile.close()
    return storedArray

def writeIdToFile(id):
    storedPostsFile = open("posts.txt", "w")
    storedPostsFile.write(id + "\n")
    storedPostsFile.close()


while True:
    posts = praw.helpers.submission_stream(r, "all")
    repliedTo = []

    try:
        repliedTo += getStoredPostIds()
    except IOError:
        print('cannot open')

    for s in posts:
        if check_condition(s) and s.id not in repliedTo:
            bot_action(s)
