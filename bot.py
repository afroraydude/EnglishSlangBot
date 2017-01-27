import praw # external stuff
import time # python stuff

from MyParser import MyParser # my stuff

reddit = praw.Reddit('bot1') # from config

subreddit = reddit.subreddit("BritBot") # testing subreddit

commented = None # delete this

def brit_convert(parent):
        c = "ERROR RECIEVED"
	try:
		f = MyParser()
		try:
			c = parent
        	except:
			print "CANNOT GET PARENT BODY"
		f.read("brit.ini")
        	d = f.as_dict()
	except:
		print "ERROR!"
	try:
		for key in d['brit']:
			new = d['brit'][key]
			string.replace(c, key, d['brit'][key])
			print new
			print c
	except:
		print "TRY AGAIN AFRO"
	return c
def check_summon(c):		
    text = c.body
    if text.find("engslang! brit") != -1:
        return True
def bot_action(c, verbose=True, respond=True):
    	test = "MessageCheck Started"
	text = c.body
    	if verbose:
    	    print test
        if respond and text.find("has been summoned") == -1:
            head = "SlangBot (English) has been summoned!\n\n"
	    tail = "\n\n[^^^I ^^^am ^^^a ^^^bot](http://reddit.com/r/britbot/)\nYou can provide feedback in my subreddit: /r/BritBot :)"
	 
            parent = c.parent()
	    try:
		check = parent.body
		fixed = brit_convert(parent.body)
		try:
                    c.reply(head + fixed + tail)
		except praw.exception.APIException:
		    print "Pausing for 2 mins"
		    time.sleep(120)
		    c.reply(head + fixed + tail)
                    with open("commented.txt", "a") as myfile:
                        myfile.write("\n" + c.id)
                
		#    print "WAS KILL"
		
            except AttributeError:
		print "is submission " + c.id
	else:
		print "is me"
		return
def hasnt_answered(c, verbose=True):
    commented = open("commented.txt").read().splitlines()
    if c.id not in commented:
        if verbose:
            print "Bot has been summoned and has not replied"
        bot_action(c)
    else:
	print "I have already answered"

for c in subreddit.stream.comments():
    if check_summon(c):
        hasnt_answered(c)
