import glob
import praw  # Reddit
import requests

def get_pics(subreddit="gaming", folder="pics/", post=25, length=45):
    '''Gets pics from desired {subreddit}\'s hot {post} posts with length <= {length} and puts into {folder}'''
    
    pics_reddit = glob.glob(folder + "*.jpeg")
    if pics_reddit != []:
        print("pics/ not empty yet")
        return 0

    c_id = "Your ID here"
    c_secret = "Your secret here"
    c_agent = "Your agent here"

    reddit = praw.Reddit(client_id=c_id,
                         client_secret=c_secret,
                         user_agent=c_agent)
    gaming = reddit.subreddit(subreddit)
    cnt = 0
    for post in gaming.hot(limit=post):
        if cnt == 10:
            break
        elif ( post.url.endswith(".jpg") or post.url.endswith(".png") ) and len(post.title) <= length:
            #print(post.link_flair_text)
            title = post.title
            title = title.replace('?', "")
            title = title.replace('.', "")
            title = title.replace('/', "")
            title = title.replace('  ', " ")
            title = title.replace(' .', ".")
            title = title.replace('"', "")

            url = post.url
            fp = folder + title + ".jpeg"
            r = requests.get(url)
            with open(fp, "wb") as f:
                f.write(r.content)
            cnt += 1
