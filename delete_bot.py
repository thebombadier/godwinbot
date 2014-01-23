import praw, time

def add_to_error(id_p):
    with open('error.txt', 'a') as file:
        file.write(id_p + '\n')
    file.close()

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
    
r = praw.Reddit('delete negative karama comments for /u/godwin_finder by /u/the_bombadier')
username = 'godwin_finder'      
r.login(username,'LYceum98')
already_done = []
read_list(already_done)
user = r.get_redditor(username)
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
                     
except:
     print "Unexpected error:", sys.exc_info()[0]
     add_to_error(traceback.format_exc())
     

