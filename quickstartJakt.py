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

information = usersFile.readline().split(",")
if len(information) > 1:
    insta_username = information[0].strip()
    insta_password = information[1].strip()
    
# set headless_browser=True if you want to run InstaPy on a server

# set these in instapy/settings.py if you're locating the
# library in the /usr/lib/pythonX.X/ directory:
#   Settings.database_location = '/path/to/instapy.db'
#   Settings.chromedriver_location = '/path/to/chromedriver'
broker_address = "localhost"
client = mqtt.Client("InstaBot")  # create new instance
client.connect(broker_address)  # connect to broker
client.loop_start()
onServer = False


while True: 
    if onServer:
        session = InstaPy(username=insta_username, password=insta_password, use_firefox=True, nogui=True, headless_browser=True, mqttClient=client)
    else:
        session = InstaPy(username=insta_username, password=insta_password, mqttClient=client)

    logger = session.get_instapy_logger(True)
    try:
            
        session.login()
        if session.aborting:
            raise Exception("Aborting login, probably bad login")

        userList = []
        userToInteractWithFile = open("interactuserlists0.txt", "r")

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
            session.set_user_interact(amount=10, randomize=True, percentage=100, media='Photo')

            for i in range(len(userList)):
                session.interact_user_followers(userList[i], amount=10, randomize=True)      # Change this to be interact_user_followers so as to interact with users who followed the listed people
                for j in range(100):
                    if j%10 == 0:
                        session.log_followers()
                    print(j)
                    sleep(36)

    except Exception as exc:
        client.publish("instapy/connected", insta_username + " is disconnected")  # publish
        logger.error("Exception caught: ", exc)
        # if changes to IG layout, upload the file to help us locate the change
        if isinstance(exc, NoSuchElementException):
            file_path = os.path.join(gettempdir(), '{}.html'.format(time.strftime('%Y%m%d-%H%M%S')))
            with open(file_path, 'wb') as fp:
                fp.write(session.browser.page_source.encode('utf8'))
            logger.error('{0}\nIf raising an issue, please also upload the file located at:\n{1}\n{0}'.format(
                '*' * 70, file_path))
            # full stacktrace when raising Github issue
            raise

    finally:
        # end the bot session
        session.end()
        sleep(600)
