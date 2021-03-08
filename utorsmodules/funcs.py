from time import time
from alive_progress import alive_bar as aliveBar
from .misc import bubbleSort, fetchPosts, findAuthor, makeSecondaryLists, removePost, satisfiesRequirements, timeCheck, valid
from .graph import graph

def countTranscriptions(
        config,
        hours,
        postsCounted,
        postsWithinTime,
        reddit,
        seconds,
        subreddits,
        subToCheck,
        totalPosts
    ):
    postList = fetchPosts(reddit, subToCheck)
    
    with aliveBar(1000, spinner='classic', bar='classic', enrich_print=False) as progress:
        for post in postList:
            if not valid(hours, post, seconds): break
            else: pass
            if satisfiesRequirements(post, subToCheck, seconds):
                totalPosts += 1
                print(f" +1 transcription on {post.title.split(' ')[0]}")
                if config["coverage"]: postsWithinTime = timeCheck(post, postsWithinTime, reddit, seconds, subToCheck)
                try:
                    subreddits[post.title.split(' ')[0]] += 1
                    postsCounted.append(post.id)
                except KeyError:
                    subreddits[post.title.split(' ')[0]] = 1
                    postsCounted.append(post.id)
            
            progress()
    
    return postsCounted, postsWithinTime, subreddits, totalPosts

def checkTranscriptions(config, reddit, subsToCheck, hours, seconds, totalPosts):
    while True:
        totalPosts = 0
        subreddits = {}
        postsWithinTime, postsCounted = [], []
        
        for subToCheck in subsToCheck:
            postsCounted, postsWithinTime, subreddits, totalPosts = countTranscriptions(
                                                                        config,                                                        
                                                                        hours,
                                                                        postsCounted,
                                                                        postsWithinTime,
                                                                        reddit,
                                                                        seconds,
                                                                        subreddits,
                                                                        subToCheck,
                                                                        totalPosts
                                                                    )
        
        subredditsList = []
        for i in subreddits: subredditsList.append([i, subreddits[i]])
        
        subredditsList = bubbleSort(subredditsList)
        subredditNames, subredditCounts = makeSecondaryLists(subredditsList, False)
        
        for i in range(len(subredditsList)): print(f" {subredditsList[i][1]} on {subredditsList[i][0]}")
        
        print(f" A total of {totalPosts} posts have been transcribed in the last {hours} hours.")
        
        if config["graph"]: graph(config, subredditCounts, subredditNames, hours, f"Total Transcriptions: {totalPosts}", "t")
        
        if config["refreshable"]: input(" Press ENTER to refresh.")
        else: return postsCounted, postsWithinTime, subredditCounts, subreddits, totalPosts
 

def checkTranscribers(config, hours, reddit, seconds, subsToCheck):

    from prawcore.exceptions import Forbidden
    from praw.exceptions import ClientException
    
    while True:    
        
        totalPosts = 0
        transcribers, authorFlairs = {}, {}
        authors = []

        for subToCheck in subsToCheck:
        
            postList = fetchPosts(reddit, subToCheck)
            successfulPosts = []
            
            for post in postList:
                if not valid(hours, post, seconds): break
                else: pass
                if satisfiesRequirements(post, subToCheck, seconds):
                    author = None
                    if subToCheck == "transcribersofreddit":
                        if not reddit.submission(url=post.url).id in successfulPosts and not post.link_flair_text in ["Unclaimed", "In Progress"]:
                            for comment in post.comments: author, authorFlairs = findAuthor(comment, authorFlairs); successfulPosts.append(post.id)
                    elif subToCheck == "tor_archive":
                        try: author = reddit.comment(url=post.url).author; successfulPosts.append(post.id)
                        except (ClientException, Forbidden, AttributeError) as e:
                            if config["verbose"]: print(e)
                            author = "Unknown"
                            successfulPosts.append(post.id)
                    if author is None:
                        for comment in post.comments:
                            for firstReply in comment.replies:
                                if firstReply.author.name == "transcribersofreddit":
                                    for secondReply in firstReply.replies:
                                        author, authorFlairs = findAuthor(secondReply, authorFlairs)
                    if not author is None:
                        totalPosts += 1
                        try:
                            print(f" +1 transcription to {author.name}")
                            try: transcribers[author.name] += 1
                            except KeyError:
                                transcribers[author.name] = 1
                                authors.append(author.name)
                        except AttributeError: print(" 1 transcription with no discernable author.")
        
        authorList = []
        
        for author in authors:
            if not author in authorFlairs:
                for comment in reddit.redditor(author).comments.new(limit=None):
                    if comment.subreddit == "transcribersofreddit":
                        flair = comment.author_flair_text.split(' ')[0]
                        print(f" Fetched flair {flair} for {author}.")
                        break
                authorFlairs[author] = flair
            
        for i in transcribers: authorList.append([i, transcribers[i], authorFlairs[i]])
        
        authorList = bubbleSort(authorList)
        authorNames, authorGamma = makeSecondaryLists(authorList, True)
        
        for i in range(len(authorList)):
            print(f" {authorList[i][1]} by {authorList[i][0]} ({authorList[i][2]})")
        
        print(f" A total of {totalPosts} posts have been transcribed in the last {hours} hours.")
        
        if config["graph"]:
            for author in authorList: authorNames[authorList.index(author)] = author[0] + f" ({author[1]})"
            graph(config, authorGamma, authorNames, hours, "Gamma", "g")
        
        if config["refreshable"]: input(" Press ENTER to refresh.")
        else: break

def coverage(
        config,
        hours,
        postsCounted,
        postsWithinTime,
        reddit,
        seconds,
        subreddits,
        totalPosts
    ):
        
    print(" \n\n COVERAGE \n\n")
    
    postList = fetchPosts(reddit, "tor_archive", verbose=config["verbose"])
    
    for post in postList:
        if post.id in postsCounted and post.id not in postsWithinTime:
            postsCounted, subreddits = removePost(post, postsCounted, subreddits, f"post older than {hours} hours.")
        
        elif post.id in postsCounted:
            if reddit.submission(reddit.comment(url=post.url).link_id.split('_')[1]).author is None:
                postsCounted, subreddits = removePost(post, postsCounted, subreddits, "post deleted/removed.")
        
        try:
            if subreddits[post.title.split(' ')[0]] == 0:
                subreddits.pop(post.title.split(' ')[0], None)
        except KeyError: pass
    
    for subreddit in subreddits:
        postList = fetchPosts(reddit, subreddit, verbose=config["verbose"])
        
        subredditCount = 0
        for post in postList:
            if time() - post.created_utc <= seconds: subredditCount += 1
            else: break
        
        try:
            print(f" {subreddit} received {subredditCount} posts in the last {hours} hours, of which {subreddits[subreddit]} were transcribed, or a coverage of {format((subreddits[subreddit] / subredditCount) * 100, '.2f')}%")
        except ZeroDivisionError:
            print(f" Could not calculate coverage for {subreddit}; division by zero.")
