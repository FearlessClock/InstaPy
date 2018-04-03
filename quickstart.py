import os
import time
from tempfile import gettempdir

from selenium.common.exceptions import NoSuchElementException

from instapy import InstaPy
from random import randrange
from time import sleep 

insta_username = 'jattecizexi9495'
insta_password = '12345Azerty'

    
# set headless_browser=True if you want to run InstaPy on a server

# set these in instapy/settings.py if you're locating the
# library in the /usr/lib/pythonX.X/ directory:
#   Settings.database_location = '/path/to/instapy.db'
#   Settings.chromedriver_location = '/path/to/chromedriver'
session = InstaPy(username=insta_username, password=insta_password,
                    headless_browser=False,
                        use_firefox=True,
                            multi_logs=True)

        
try:
        
    session.login()

    # set up all the setting
    session.set_do_comment(False, percentage=0)
    session.set_use_clarifai(enabled=False)
    # do the actual liking
    while True:
        #Strategy 1: Hashtab
        tagsList = ['bluemerle', 'bluemerlepom', 'bluemerlepomeranian', 'dogstagram', 'dogoftheday', 'pupsofinstagram', 'pup', '6weeksold', 'sleepypuppy', 'pominu', 'puppyboots', 'boots', 'spots', 'bluemerlepom', 'bluemerle', 'pomeranianshibainu', 'shibainu', 'pomeranianpuppy'\
                'sleepingpuppy', 'puppybaby', 'doggystyle', 'thedogslife', 'thedoggycalendar', 'littlebabe', 'littledog', 'designerdog', 'mix', 'shibainupuppy', 'shibainu', 'pominu', 'pom', 'pomeranianpuppy', 'pomeranian', 'puppiesofig']

        for i in range(len(tagsList)):
            session.like_by_tags([tagsList[i]], amount=randrange(30, 70))
            sleep(3600)
        
        #strategy 2: Follower liking
        session.set_user_interact(amount=10, random=True, percentage=100, media='Photo')
        session.set_do_like(enabled=True, percentage=100)
        session.set_do_follow(enabled=True, percentage=100)

        userList = ['jiffpom', 'pomeranianworld', 'mr.monsterpup', 'thedogist', 'dogsofinstagram']
        for i in range(len(userList)):
            session.interact_user_followers([userList[i]], amount=randrange(10, 40), random=True)
            sleep(3600)

except Exception as exc:
    # if changes to IG layout, upload the file to help us locate the change
    if isinstance(exc, NoSuchElementException):
        file_path = os.path.join(gettempdir(), '{}.html'.format(time.strftime('%Y%m%d-%H%M%S')))
        with open(file_path, 'wb') as fp:
            fp.write(session.browser.page_source.encode('utf8'))
        print('{0}\nIf raising an issue, please also upload the file located at:\n{1}\n{0}'.format(
            '*' * 70, file_path))
    # full stacktrace when raising Github issue
    raise

finally:
    # end the bot session
    session.end()
