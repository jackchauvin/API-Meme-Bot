#--------------------------------------------------------------------
#           Meme Poster for Instagram, Twitter, and Facebook
# 
#           Jack Chauvin - May 2020
#--------------------------------------------------------------------
import glob
import time
from time import sleep
import os
from os import listdir

import redditPics  # Reddit
from instabot import Bot # Instabot

def oldest_pic(folder= "pics/"):
    pics = glob.glob(folder + "*.jpeg")
    now = time.time()
    oldest = pics[0], now - os.path.getctime(pics[0])
    for pic in pics[1:]:
        age = now - os.path.getctime(pic)
        if age > oldest[1]:
            oldest = pic, age
    return oldest[0]

def remove_pics(pic_title, fold="pics/"):
    folder = os.listdir(fold)
    for item in folder:
        if item.endswith(".REMOVE_ME") or pic_title in item:
            os.remove(fold+item)


# Load Instabot
bot = Bot()
insta_usr = "YOUR USERNAME"
insta_pass = "YOUR PASSWORD"
bot.login(username= insta_usr, password= insta_pass)

timeout = 12 * 60 * 60  # pics will be posted every 12 hours

while True:
    
    try:
        print("Beginning next post...")
        print("Getting pics from Reddit...")
        redditPics.get_pics(subreddit= "gaming")

        # Find oldest pic & Post
        pic = oldest_pic().split('/')[-1]  # Gets pic file name
        pic_name = pic[:-5]  #gets rid of ".jpeg"
        print("uploading: " + pic)
      
        # Post data
        fp = "pics/" + pic
        desc = pic_name + "\n------------\nFollow for DAILY MEMES\n------------\n"
        small_tags = "#gaming #gamingsetup #gaminingmemes #gamingpc #gamingcommunity #pcmasterrace #pcgaming #games #gaming #gamingmeme #memes #meme"
        long_tags = "#gamingmemes #gamingmeme #gamingrig #gamingcommunity #gamingroom #gamingislife #gamingnews #gamingposts #gamingsetup #gamingphotography #gamingpc #gaminglife #videogaming #consolegaming #fortnitegaming #xboxmemes #gamesworkshop #epicgames #pubgmemes #gamerlife #gamersunite #playstation #girlgamer #gamersofinstagram #gamingpc #playstationmemes #gamergeek #relationship #girlgamers #instamemes"

        # Uploads picture to Instagram
        print("Posting to Instagram...")
        insta_desc = desc + long_tags
        bot.api.upload_photo(fp, caption=insta_desc, force_resize=True)

        if bot.api.last_response.status_code != 200:
            print(bot.api.last_response)
            # send msg

        # Removes sent pictures
        print("Removing posted photos...")
        remove_pics(pic)
        print("Done...\nGoing to sleep...")
        time.sleep(timeout)
        
    except Exception as e:
        print(str(e))
        print("Error, removing pic and timing out...")
        remove_pics(pic)
        time.sleep(timeout)