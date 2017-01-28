import praw # external stuff
import time # python stuff
import sys

from MyParser import MyParser # my stuff

reddit = praw.Reddit('bot1') # from config

subreddit = reddit.subreddit("BritBot") # testing subreddit

commented = None # delete this

def usn_convert(parent):
        hasUSN = False
        c = "ERROR RECIEVED"
        f = MyParser()
        f.read('slanglib.ini')
        words = f.as_dict()
        try:
                c = parent
                for key in words['usn']:
                        c = c.replace(key, words['usn'][key])
                        hasUSN = True
        except:
                print "CANNOT GET PARENT BODY"
        if hasUSN:
                print "Translated"
        else:
                c = "There is no british slang here!"
        return c

def brit_convert(parent):
	hasBrit = False
        c = "ERROR RECIEVED"
	f = MyParser()
	f.read('slanglib.ini')
	words = f.as_dict()
	try:
		c = parent
		for key in words['brit']:
			c = c.replace(key, words['brit'][key])
       			hasBrit = True
	except:
		print "CANNOT GET PARENT BODY"
	if hasBrit:
		print "Translated"
	else:
		c = "There is no british slang here!"
	return c
def check_summon(c):		
    text = c.body
    if text.find("engslang!") != -1:
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
		if text.find("brit") != -1:
			fixed = "Translation: " + brit_convert(parent.body) 
		else:
		    print "Command does not exist"
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
		print "is submission or error, comment id " + c.id
	else:
		print "is me"
		return
def check_post(s):
	try:
		author = str(s.author.name)
		return True
	except:
		return False
def hasnt_answered(c, verbose=True):
    commented = open("commented.txt").read().splitlines()
    if c.id not in commented and check_post:
        if verbose:
            print "Bot has been summoned and has not replied"
        bot_action(c)
    else:
	print "I have already answered"

for c in subreddit.stream.comments():
    if check_summon(c):
        hasnt_answered(c)
