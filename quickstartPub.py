from instapy import InstaPy
from random import randrange
from time import sleep 

insta_username = 'pierothepup'
insta_password = 'spooky12!'

# if you want to run this script on a server, 
# simply add nogui=True to the InstaPy() constructor
session = InstaPy(username=insta_username, password=insta_password, use_firefox=True)
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
    session.set_user_interact(amount=10, randomize=True, percentage=100, media='Photo')
    session.set_do_like(enabled=True, percentage=100)
    session.set_do_follow(enabled=True, percentage=100)

    userList = ['jiffpom', 'pomeranianworld', 'mr.monsterpup', 'thedogist', 'dogsofinstagram']
    for i in range(len(userList)):
        session.interact_user_followers([userList[i]], amount=randrange(10, 40), randomize=True)
        sleep(3600)

# end the bot session
session.end()
