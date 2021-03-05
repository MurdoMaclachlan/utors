from time import time

"""
    This module contains functions not easily
    categorised into other modules.
"""

def bubbleSort(array):
    isSorted = False
    while not isSorted:
        isSorted = True
        for i in range(len(array)-1):
            if array[i][1] > array[i+1][1]:
                temp = array[i]
                array[i] = array[i+1]
                array[i+1] = temp
                isSorted = False
    return array

def fetchPosts(reddit, subreddit, verbose=True):
    if verbose: print(f" Fetching posts from {subreddit}...")
    postList = reddit.subreddit(subreddit).new(limit=None)
    if verbose: print(" Posts fetched; generating list...")
    return postList

def findAuthor(comment, authorFlairs):
    if removeNonAlpha(comment.body.casefold()) == "done":
        for reply in comment.replies:
            if "Awesome" in reply.body.split(' ,') and reply.author.name == "transcribersofreddit":
                if not comment.author.name in authorFlairs: authorFlairs[comment.author.name] = comment.author_flair_text; print(f" Found flair {comment.author_flair_text} for {comment.author.name}.")
                return comment.author, authorFlairs
    return None, authorFlairs

def makeSecondaryLists(dictionary, simple):
    x,y = [], []
    for i in dictionary:
        x.append(i[0] if simple else f" {i[0]} ({i[1]})")
        y.append(i[1])
    return x, y

def removeNonAlpha(comment):
    charArray = list(comment)
    newArray = []
    for i in charArray:
        if i.isalpha():
            newArray.append(i)
    return ''.join(newArray)

def removePost(post, postsCounted, subreddits, s):
    print(f" -1 transcription on {post.title.split(' ')[0]}; {s}")
    postsCounted.pop(postsCounted.index(post.id))
    try:
        subreddits[post.title.split(' ')[0]] -= 1
    except KeyError: pass
    return postsCounted, subreddits

def satisfiesRequirements(post, subToCheck, seconds):
    from time import time
    if time() - post.created_utc < seconds:
        if subToCheck == "tor_archive": return True
        elif post.link_flair_text == "Completed!": return True
        else: return False
    return False

"""
    ONE-LINE functions.
    
    These are mostly here to make the more top-level
    modules more easily readable.**
"""

def strToBool(s):
    return s.casefold() in ("yes", "y", "true", "t", "1")

def timeCheck(post, postsWithinTime, reddit, seconds, subToCheck):
    if subToCheck == "tor_archive" and time() - reddit.submission(reddit.comment(url=post.url).link_id.split('_')[1]).created_utc < seconds: postsWithinTime.append(post.id); return postsWithinTime
    else: return postsWithinTime

def valid(hours, post, seconds):
    if time() - post.created_utc > seconds: print(f" Passed the {hours} hour mark, stopping analysis."); return False
    else: return True
