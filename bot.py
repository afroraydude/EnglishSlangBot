# TODO: VERBOSITY
import praw # external stuff
import time # python stuff
import sys # delete this

from MyParser import MyParser # my stuff

reddit = praw.Reddit('bot1') # from config

subreddit = reddit.subreddit("BritBot") # testing subreddit

commented = None # delete this

def us_convert(parent):
        hasUS = False
        c = "ERROR RECIEVED"
        f = MyParser()
        f.read('slanglib.ini')
        words = f.as_dict()
        try:
                c = parent
                for key in words['us']:
                        c = c.replace(key, words['us'][key])
                        hasUS = True
        except:
                print "CANNOT GET PARENT BODY"
        if hasUS:
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
		c = parent # parent comment's body (what we translate)
		for key in words['brit']: # all words in the British slang list
			c = c.replace(key, words['brit'][key]) # Replaces the word with the translation 
       			hasBrit = True # See below for usage
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
    	if verbose:
		test = "MessageCheck Started" 
	text = c.body
    	if verbose:
    	    print test
        if respond and text.find("has been summoned") == -1:
            head = "SlangBot (English) has been summoned!\n\n" # Begining of message
	    tail = "\n\n[^^^I ^^^am ^^^a ^^^bot](http://reddit.com/r/britbot/)\nYou can provide feedback in my subreddit: /r/BritBot :)" # end of message
	 
            parent = c.parent()
	    try:
		check = parent.body
		if text.find("brit") != -1:
			fixed = "Translation: " + brit_convert(parent.body) 
		else:
			if text.find("us") != -1:
				fixed = "Translation: " + us_convert(parent.body)
		
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
		if verbose:
			print "is submission or error, comment id " + c.id
	else:
		if verbose:
			print "is me"
		return
def check_post(s, verbose=True):
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
	if verbose:
		print "I have already answered"

for c in subreddit.stream.comments():
    if check_summon(c):
        hasnt_answered(c)
