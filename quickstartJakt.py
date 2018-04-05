import os
import time
from tempfile import gettempdir

from selenium.common.exceptions import NoSuchElementException

from instapy import InstaPy
from random import randrange
from time import sleep 
import paho.mqtt.client as mqtt


insta_username = None
insta_password = None
usersFile = open("users.txt", "r")

information = usersFile.read().split(",")
if len(information) > 1:
    insta_username = information[0]
    insta_password = information[1]
    
# set headless_browser=True if you want to run InstaPy on a server

# set these in instapy/settings.py if you're locating the
# library in the /usr/lib/pythonX.X/ directory:
#   Settings.database_location = '/path/to/instapy.db'
#   Settings.chromedriver_location = '/path/to/chromedriver'
broker_address = "localhost"
client = mqtt.Client("InstaBot")  # create new instance
client.connect(broker_address)  # connect to broker
client.loop_start()
session = InstaPy(username=insta_username, password=insta_password,use_firefox=True, nogui=True, headless_browser=True, mqttClient=client)

        
try:
        
    session.login()

    userList = []
    userToInteractWithFile = open("interactuserlists.txt", "r")

    for line in userToInteractWithFile:
        userList.append(line.strip())


    # set up all the setting
    session.set_do_comment(False, percentage=0)
    #session.set_use_clarifai(enabled=False)
    # do the actual liking
    while True:
        #strategy 1: Follower liking
        session.set_do_like(enabled=True, percentage=70)
        session.set_do_follow(enabled=True, percentage=100)

        session.interact_by_users(userList, amount=40, randomize=True)
        for j in range(100):
            session.log_followers()
            print(j)
            sleep(36)

except Exception as exc:
    client.publish("instapy/connected", "disconnected")  # publish
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
