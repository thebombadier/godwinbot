import praw, time, datetime, sys, logging, traceback



logging.basicConfig(filename='whole.log',level=logging.WARNING)



def login(name,password):
    try:
        r.login(name,password)
        return "Logged in as: " + name
    except:
        return "Error"
    
def add_to_error(id_p):
    with open('error.txt', 'a') as file:
        file.write(id_p + '\n')
    file.close()

def add_to_list(id_p):
    with open('posts.txt', 'a') as file:
        file.write(id_p + '\n')
    file.close()

def add_to_ban(id_p):
    with open('ban.txt', 'a') as file:
        file.write(id_p + '\n')
    file.close()
    r.edit_wiki_page('godwinbot','ban',"* " + id_p + "\n\n",'I was banned from' + id_p)
    
def read_list(var):
    f = open('posts.txt', 'r')
    for line in f:
        var.append(line)
    f.close()

def read_ban(var):
    f = open('ban.txt', 'r')
    for line in f:
        var.append(line)
    f.close()

def handle_ratelimit(func, *args, **kwargs):
    while True:
        try:
            func(*args, **kwargs)
            break
        except praw.errors.RateLimitExceeded as error:
            print '\tSleeping for %d seconds' % error.sleep_time
            time.sleep(error.sleep_time)
    
def contains(selftext,words,sub_id,submission,done):
    badsubs = []
    read_ban(badsubs)
    some = 0
    read_list(done)
    amount = 0
    has_nazi_text = any(string in selftext.lower() for string in words)
    has_nazi_title = any(string in submission.title.lower() for string in words)
    if sub_id + '\n' not in done and str(submission.subreddit) not in badsubs:
        add_to_list(submission.id)
        done.append(submission.id)
        if has_nazi_text or has_nazi_title:
            some = 0
            
            return "Nazi referenced in submission: " + submission.title + " so no comment made " 
            
            
        flat = praw.helpers.flatten_tree(submission.comments)
        for comment in flat:
            amount = amount + 1
            for nazi in words:
                if not hasattr(comment, 'body'):
                    continue
                if nazi in comment.body.lower() :
                    some = 1
                    time1 =  comment.created_utc - submission.created_utc
                    if amount > 1:
                        text = " comments"
                    else:
                        text = " comment"
                    try:
                        
                        comment.reply("It took this thread " + datetime.datetime.fromtimestamp(time1).strftime("%H hours, %M minutes, %S seconds") + " and " + str(amount) + text + " to make a reference to the nazis, for more information look up [Godwin's Law] (http://en.wikipedia.org/wiki/Godwin's_law). \n *** \n  *^[about](http://www.reddit.com/r/godwinbot/wiki/index) ^| ^/u/" + comment.author.name + " ^can ^reply ^with ^'delete' ^to ^delete ^this ^comment. ^Additionally, ^if ^this ^gets ^a ^score ^of ^-1 ^after ^30 ^minutes ^this ^comment ^will ^be ^deleted.*" )
                        return "Nazi reference in comment by " + comment.author.name + " Comment: " + comment.body
                        time.sleep(300)
                        break
                    except praw.errors.RateLimitExceeded as e:
                        print 'Sleeping for ' + str(e.sleep_time) + ' seconds'
                        time.sleep(e.sleep_time)
                    except Exception as e:
                        add_to_error("REPLY FAILED: %s @ %s"%(e,submission.subreddit))
                        if str(e) == '403 Client Error: Forbidden':
                            badsubs.append(str(submission.subreddit))
                            add_to_ban(str(submission.subreddit))
                            return "Banned from this subreddit"
                    except Exception as e:
                        add_to_error(e)
                        return "Unidentified error"
                        
                
                    
                    
                    
                    
                    
    if some == 0:
        return "No Nazi reference found"
        
        
            
r = praw.Reddit("Godwin's Law bot by /u/the_bombadier"
                "http://www.github.com/thebombadier/godwinbot"
                )
print login('username','password')

subreddit = r.get_subreddit('all')
try:
    while True:
        words = ["nazi", "hitler"]
        done = []
        read_list(done)
        for submission in subreddit.get_hot(limit=50):
            
            if submission.id + '\n' not in done:
                submission.replace_more_comments(limit=8, threshold=5)
            
                print contains(submission.selftext.lower(),words,submission.id,submission,done)
except:
     print "Unexpected error:", sys.exc_info()[0]
     add_to_error(traceback.format_exc())
     time.sleep(500)
