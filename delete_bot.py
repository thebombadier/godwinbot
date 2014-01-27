import praw, time

def add_to_error(id_p):
    with open('error.txt', 'a') as file:
        file.write(id_p + '\n')
    file.close()

def read_ban(var):    
    f = open('ban.txt', 'r')    
    for line in f:        
        var.append(line)    
        f.close()

def add_to_delete(id_p):
    with open('delete.txt', 'a') as file:
        file.write(id_p + '\n')
    file.close()
    
def add_to_done(id_p):
    with open('done.txt', 'a') as file:
        file.write(id_p + '\n')
    file.close()

def read_list(var):
    f = open('done.txt', 'r')
    for line in f:
        var.append(line)
    f.close()
    
def add_to_ban(id_p,badsubs):    
    with open('ban.txt', 'a') as file:        
        file.write(id_p + '\n')    file.close()
        if id_p not in badsubs:
            wiki = r.get_wiki_page('godwinbot','ban')
            r.edit_wiki_page('godwinbot','ban',wiki.content_md + "\n\n * **" + id_p + "**",'I was banned from' + id_p)
        else:
            return "Already Banned"
r = praw.Reddit('delete negative karama comments for /u/godwin_finder by /u/the_bombadier')
username = 'username'      
r.login(username,'password')
already_done = []
read_list(already_done)
user = r.get_redditor(username)
badsubs = []
read_ban(badsubs)
try:
    while True:
        for c in user.get_comments(limit=None):
            if time.time() - c.created_utc > 1800:
                if c.score < 0 and c.id not in already_done:
                    c.delete()
                    print 'Deleted Comment in subreddit: ' + c.subreddit.display_name + " score of " + str(c.score)
                    perm = str(c.permalink) + " Score: " + str(c.score)
                    add_to_delete(perm)
                    already_done.append(c.id) 
                    add_to_done(c.id)
        unread = r.get_unread(limit=None)
        for msg in unread:
            if msg.body.lower() == "delete":
                bot_comment_id = msg.parent_id
                bot_comment = r.get_info(thing_id=bot_comment_id)
                person_comment = r.get_info(thing_id=bot_comment.parent_id)
                if msg.author.name == person_comment.author.name and bot_comment.id not in already_done:
                    bot_comment.delete()
                    print "Deleted comment because " + person_comment.author.name + " replied with delete "
                    perm = str(bot_comment.permalink) + " User " + person_comment.author.name + " replied with delete"    
                    add_to_delete(perm)
                    already_done.append(bot_comment.id) 
                    add_to_done(bot_comment.id)
            if "you have been banned from posting to " in msg.body.lower():
                if "/r/" + msg.athor.name  in msg.body.lower() and msg.author.name not in badsubs:
                    sub = r.get_subreddit(str(msg.author.name))
                    try:
                        for post in sub.get_hot(limit=1):
                            return "Not Banned"
                    except Exception as e:
                        if str(e) == '403 Client Error: Forbidden':
                            return "Baned from: " + msg.author.name
                            add_to_ban(str(msg.author.name),badsubs)
                            
                     
except:
     print "Unexpected error:", sys.exc_info()[0]
     add_to_error(traceback.format_exc())
     

