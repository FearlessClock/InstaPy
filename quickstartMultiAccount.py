import datetime
import os
import time
from tempfile import gettempdir

import multiprocessing
from selenium.common.exceptions import NoSuchElementException

from instapy import InstaPy
from random import randrange
from time import sleep
import paho.mqtt.client as mqtt

insta_usernames = []
insta_passwords = []
usersFile = open("users.txt", "r")

information = usersFile.readline().split(",")
while len(information) > 1:
    insta_usernames.append(information[0].strip())
    insta_passwords.append(information[1].strip())
    information = usersFile.readline().split(",")

# set headless_browser=True if you want to run InstaPy on a server

# set these in instapy/settings.py if you're locating the
# library in the /usr/lib/pythonX.X/ directory:
#   Settings.database_location = '/path/to/instapy.db'
#   Settings.chromedriver_location = '/path/to/chromedriver'
onServer = False

def worker(username, password, index):
    broker_address = "localhost"
    client = mqtt.Client(username)  # create new instance
    client.connect(broker_address)  # connect to broker
    client.loop_start()

    client.publish("instapy/connected", username + " is connected")  # publish


    print("MULTI - Started as", username, "at", datetime.datetime.now().strftime("%H:%M:%S"))
    tagFile = open("taglists"+str(index)+".txt", "r")

    tagsList = []
    for line in tagFile:
        tagsList.append(line.strip())

    userList = []
    userToInteractWithFile = open("interactuserlists"+str(index)+".txt", "r")

    for line in userToInteractWithFile:
        userList.append(line.strip())

    while True:
        try:
            if onServer:
                session = InstaPy(username=username, password=password, use_firefox=True, nogui=True, headless_browser=True, mqttClient=client, multi_logs=True)
            else:
                session = InstaPy(username=username, password=password, mqttClient=client)

            logger = session.get_instapy_logger(True)
            logger.info("Logging in!")
            session.login()
            # set up all the setting
            session.set_do_comment(False, percentage=0)
            # session.set_use_clarifai(enabled=False)
            # do the actual liking

            # Strategy 1: Hashtab
            if len(tagsList) > 0:
                for i in range(len(tagsList)):
                    logger.info("Starting on tag: " + tagsList[i])
                    session.like_by_tags([tagsList[i]], amount=randrange(30, 70))
                    for j in range(100):
                        if j % 10 == 0:
                            session.log_followers()
                        print(j)
                        sleep(36)

            # strategy 2: Follower liking
            session.set_user_interact(amount=10, randomize=True, percentage=100, media='Photo')
            session.set_do_like(enabled=True, percentage=100)
            session.set_do_follow(enabled=True, percentage=100)
            if len(userList) > 0:
                for i in range(len(userList)):
                    logger.info("Starting on user: " + userList[i])
                    session.interact_user_followers([userList[i]], amount=randrange(10, 40), randomize=True)
                    for j in range(100):
                        if j % 10 == 0:
                            session.log_followers()
                        print(j)
                        sleep(36)

        except Exception as exc:
            client.publish("instapy/connected", username + " is disconnected")  # publish
            logger.error("Something really went wrong with " + username);
            # if changes to IG layout, upload the file to help us locate the change
            if isinstance(exc, NoSuchElementException):
                file_path = os.path.join(gettempdir(), '{}.html'.format(time.strftime('%Y%m%d-%H%M%S')))
                logger.error(file_path)
                with open(file_path, 'wb') as fp:
                    fp.write(session.browser.page_source.encode('utf8'))
                print('{0}\nIf raising an issue, please also upload the file located at:\n{1}\n{0}'.format(
                    '*' * 70, file_path))

        finally:
            # end the bot session
            session.end()
            sleep(320)

if __name__ == '__main__':
    print("MULTI -","Starting at",datetime.datetime.now().strftime("%H:%M:%S"))
    jobs = []
    for i in range(len(insta_usernames)):
        p = multiprocessing.Process(target=worker, args=(insta_usernames[i], insta_passwords[i], i,))
        jobs.append(p)
        p.start()
        time.sleep(66);#no delay cause some instances of chrome to give errors and stop