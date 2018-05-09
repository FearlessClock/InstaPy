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
onServer = False

try:

    tagFile = open("taglists0.txt", "r")

    tagsList = []
    for line in tagFile:
        tagsList.append(line.strip())

    userList = []
    userToInteractWithFile = open("interactuserlists0.txt", "r")

    for line in userToInteractWithFile:
        userList.append(line.strip())

    while True:
        if onServer:
            session = InstaPy(username=insta_username, password=insta_password, use_firefox=True, nogui=True,
                              headless_browser=True, mqttClient=client)
        else:
            session = InstaPy(username=insta_username, password=insta_password, mqttClient=client)

        logger = session.get_instapy_logger(True)
        logger.info("Logging in!")
        session.login()
        # set up all the setting
        session.set_do_comment(False, percentage=0)
        # session.set_use_clarifai(enabled=False)
        # do the actual liking

        # settings
        session.set_relationship_bounds(enabled=True,
                     potency_ratio=None,
                      delimit_by_numbers=True,
                       max_followers=90000,
                        max_following=90000,
                         min_followers=45,
                          min_following=77)
        session.set_do_comment(True, percentage=10)
        session.set_comments(['aMEIzing!', 'So much fun!!', 'Nicey!'])
        session.set_dont_include(['friend1', 'friend2', 'friend3'])
        session.set_dont_like(['pizza', 'girl'])

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

        for i in range(len(userList)):
            logger.info("Starting on user: " + userList[i])
            session.interact_user_followers([userList[i]], amount=randrange(10, 40), randomize=True)
            for j in range(100):
                if j % 10 == 0:
                    session.log_followers()
                print(j)
                sleep(36)

except Exception as exc:
    try:
        client.publish("instapy/connected", insta_username + " is disconnected")  # publish
        logger.error("Exception caught: ", exc)
    except:
        print("Client or logger not initialized")
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
