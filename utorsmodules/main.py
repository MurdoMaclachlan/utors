import praw
from .funcs import checkTranscriptions, coverage, checkTranscribers#, checkClaim
from .args import checkArgs

def everything():
    
    version = "0.4-beta"
    
    config = checkArgs()
    seconds = config["period"]*3600
    
    print("THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR"
          "IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,"
          "FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE"
          "AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER"
          "LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,"
          "OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE"
          "SOFTWARE."
    )
    print(f" Running ToR Transcription Counter version {version}.")

    reddit = praw.Reddit("ttc", user_agent="ttc:v" + version + ":Linux:MurdoMaclachlan")
    
    subsToCheck = ["tor_archive", "transcribersofreddit"]
    totalPosts = 0
    
    #functions = {
     #   "checkTranscriptions": checkTranscriptions,
     #   "coverage": coverage,
     #   "checkTranscribers": checkTranscribers,
       # "checkClaim": checkClaim
    #}
    
    if config["transcriptions"]: postsCounted, postsWithinTime, subredditCounts, subreddits, totalPosts = checkTranscriptions(config, reddit, subsToCheck, config["period"], seconds, totalPosts)
    if config["coverage"]: coverage(config, config["period"], postsCounted, postsWithinTime, reddit, seconds, subreddits, totalPosts)
    if config["transcribers"]: checkTranscribers(config, config["period"], reddit, seconds, subsToCheck)

"""
if args["checkClaim"]:
    
    print(f" Fetching comments from {args['user']}...")
    commentList = reddit.redditor(args["user"]).comments.new(limit=None)
    print(" Posts fetched; generating list...")
    
    doneCount, claimCount, unclaimCount = 0, 0, 0
    
    for comment in commentList:
      
        if time.time() - comment.created_utc < seconds:
            if comment.body.casefold() in ["done", "done."]:
                doneCount += 1
                print(" +1 done")
            elif comment.body.casefold() in ["claim", "claiming", "claiming."]:
                claimCount += 1
                print(" +1 claim")
            elif comment.body.casefold() in ["unclaim", "unclaiming", "unclaiming."]:
                unclaimCount += 1
                print(comment.permalink)
                print(" +1 unclaim")
        elif time.time() - comment.created_utc > seconds:
            print(f" Passed the {hours} hour mark, stopping analysis.")
            break
        
    print(f" {args['user']} has claimed {claimCount} posts and finished {doneCount} of them, unclaiming {unclaimCount} of them.")
    print(f" A difference of {claimCount - doneCount}.")

transcriptionCounter()
"""
