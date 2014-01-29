import praw, time, datetime, sys, logging, traceback



logging.basicConfig(filename='whole.log',level=logging.WARNING)



def login():
    name = raw_input("Username: ")
    password = raw_input("Password: ")
    try:
	r.login(name,password)
	return "Logged in as: " + name
    except:
	return "Error"

def a(test_str):
    ret = ''
    skip1c = 0
    skip2c = 0
    for i in test_str:
        if i == '[':
            skip1c += 1
        elif i == '(':
            skip2c += 1
        elif i == ']' and skip1c > 0:
            skip1c -= 1
        elif i == ')'and skip2c > 0:
            skip2c -= 1
        elif skip1c == 0 and skip2c == 0:
            ret += i
    return ret

    
def add_to_error(id_p):
    with open('error.txt', 'a') as file:
	file.write(id_p + '\n')
    file.close()

def add_to_list(id_p):
    with open('posts.txt', 'a') as file:
	file.write(id_p + '\n')
    file.close()

def read_ban(var):
    f = open('ban.txt', 'r')
    for line in f:
	var.append(line)
    f.close()

def add_to_ban(id_p,badsubs):  
    read_ban(badsubs)  
    with open('ban.txt', 'a') as file:	      
	file.write(id_p + '\n')	   
    file.close()
    if id_p + '\n' not in badsubs:
	wiki = r.get_wiki_page('godwinbot','ban')
	print wiki.content_md + "* **" + id_p + "**"
	r.edit_wiki_page('godwinbot','ban',wiki.content_md + "\n\n* **" + id_p + "**",'I was banned from' + id_p)
	time.sleep(60) 
    else:
	return "Already Banned"
    
def read_list(var):
    f = open('posts.txt', 'r')
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
	global amount
	global nazi_co
	amount = 0
	com_word = ""
	nazi_co = 0
	global sub_post
	global time_com
	global time_sub
	global com_body
	global com_name
	global com
	nazi = ["holocaust","jews","nazi","hitler","ww2","racism","antisemitism","ethnic","cleansing","semitism"]
	if sub_id + '\n' not in done and str(submission.subreddit) not in badsubs and len(selftext)< 4000:
		has_nazi_text = any(string in selftext.lower() for string in words)
		has_nazi_title = any(string in submission.title.lower() for string in nazi)
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
				if nazi in repr(comment.body.lower()):
					nazi_co = nazi_co + 1
					if nazi_co == 1:
							sub_post = submission.subreddit
							time_com = comment.created_utc
							time_sub = submission.created_utc
							com_body = comment.body
							com_name = comment.author.name
							com = comment
		if nazi_co < 5 and nazi_co > 0:
			print"money"
			some = 1
			
			if amount > 1:
				com_word = " comments"
				print com_word
			else:
				com_word = " comment"
				print com_word
			try:
				print "why"
				time1 =	 time_com - time_sub
				com.reply("It took this thread " + datetime.datetime.fromtimestamp(time1).strftime("%H hours, %M minutes, %S seconds") +  " and " + str(amount) + str(com_word) + " to make a reference to the nazis, for more information look up [Godwin's Law] (http://en.wikipedia.org/wiki/Godwin's_law). \n *** \n  *^[about](http://www.reddit.com/r/godwinbot/wiki/index) ^| ^[source](https://www.github.com/thebombadier/godwinbot) ^| ^/u/" + str(com_name) + " ^can ^reply ^with ^'delete' ^to ^delete ^this ^comment. ^Additionally, ^if ^this ^gets ^a ^score ^of ^-1 ^after ^30 ^minutes ^this ^comment ^will ^be ^deleted.*" )
				
				
				return "Nazi reference in comment by " + com_name + " Comment: " + com_body
				time.sleep(300)
				
			except praw.errors.RateLimitExceeded as e:
				print 'Sleeping for ' + str(e.sleep_time) + ' seconds'
				time.sleep(e.sleep_time)
			except Exception as e:
				add_to_error("REPLY FAILED: %s @ %s"%(e,sub_post))
				if str(e) == '403 Client Error: Forbidden':

					add_to_ban(str(sub_post),badsubs)
					badsubs.append(str(sub_post))

					return "Banned from this subreddit"
			except Exception as e:
				add_to_error(e)
				return "wtf"
				return str(e)
		elif nazi_co > 5:
			return "Too many comments about nazis"		    
	if some == 0:
		return "No Nazi reference found"
    
	
	

	    
r = praw.Reddit("Godwin's Law bot by /u/the_bombadier"
		"http://www.github.com/thebombadier/godwinbot"
		)



print login()




while True:
    try:
	words = ["nazi", "hitler"]
	done = []
	read_list(done)
	number = 1
	for comment in praw.helpers.comment_stream(r,'all', limit = None):
	    if comment.submission.id + '\n' not in done:
		post = comment.submission
		selftext = post.selftext.lower()
	    
		print contains(selftext,words,post.id,post,done)
    except:
	 print "Unexpected error:", traceback.format_exc()
	 add_to_error(traceback.format_exc())
	 time.sleep(500)
