from instapy import InstaPy
from random import randrange
from time import sleep 

insta_username = 'jattecizexi9495'
insta_password = '12345Azerty'

# if you want to run this script on a server, 
# simply add nogui=True to the InstaPy() constructor
session = InstaPy(username=insta_username, password=insta_password)
session.login()

# set up all the setting
session.set_do_comment(False, percentage=0)

# do the actual liking
#Strategy 1: Hashtab
session.like_by_tags(['entrepreneur'], amount=randrange(30, 70))
sleep(3600)
session.like_by_tags(['entrepreneurlife'], amount=randrange(30, 70))
sleep(3600)
session.like_by_tags(['digitalagency'], amount=randrange(30, 70))
sleep(3600)
session.like_by_tags(['agencyowner'], amount=randrange(30, 70))
sleep(3600)
session.like_by_tags(['entrepreneursofinstagram'], amount=randrange(30, 70))
sleep(3600)


# end the bot session
session.end()
