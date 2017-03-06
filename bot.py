# TODO: VERBOSITY
# ^ DONE! :)

import praw # external stuff
import time # python stuff
import sys # delete this

from MyParser import MyParser # my stuff

reddit = praw.Reddit('bot1') # from config

subreddit = reddit.subreddit("all") # testing subreddit

commented = None # delete this

def convert(parent,verbose=True,slang):
    hasCa = False
    c = "None"
    f = MyParser()
    f.read('slanglib.ini')
    words = f.as_dict()
    try:
        c = parent
        for key in words['ca']:
            oldc = c
            c = c.replace(key, words[slang][key])
            if oldc != c:
                hasCa = True
    except:
        print "Cannot get body"
    if hasCa:
        if verbose:
            print "Translated"
    else:
        c = "There is nothing to translate"
    return c
def check_subs(c, verbose=True):
    appsubs = open("subs.txt").read().splitlines()
    post = c.submission
    subreddit = post.subreddit
    sname = subreddit.display_name
    if sname in appsubs:
        print "Subreddit " + sname + " is an approved subreddit"
        return True
    else:
        if verbose:
            print "Subreddit " + sname + " is not approved :("
        return False
def warn_user(c):
    user = c.author
    subreddit = c.subreddit
    try:
        user.message("From English Slang Bot Creator", "English Slang Bot hasn't been aproved for the requested subreddit.\n\nPlease have the moderators contact /u/afroraydude or post in /r/BritBot or place an issue on [here](http://github.com/afroraydude/EnglishSlangBot)", from_subreddit=subreddit)
    except:
        print "Error while trying"
def do_work(c):
    text = c.body
    if text.find("engslang!") != -1 and check_subs(c) and hasnt_answered:
        bot_action(c)
    else:
        if text.find("engslang!") != -1 and hasnt_answered(c):
            warn_user(c)
        # Else do nothing
def bot_action(c, verbose=True, respond=True):
    	if verbose:
		test = "MessageCheck Started"
	text = c.body
    	if verbose:
    	    print test
        if respond and text.find("has been summoned") == -1: # If it is me
            head = "SlangBot (English) has been summoned!\n\n" # Begining of message
	    tail = "\n\n[^^^I ^^^am ^^^a ^^^bot](http://reddit.com/r/britbot/) created by /u/afroraydude \nYou can provide feedback in my subreddit: /r/BritBot :)" # end of message

            parent = c.parent()
	    try:
		check = parent.body
		if text.find("brit") != -1: # If you use the Brit command
			fixed = "Translation: " + convert(parent.body,"brit")
		else: # For other commands
			if text.find("us") != -1: # US command
				fixed = "Translation: " + us_convert(parent.body,"us")

			else: # Any command that is not registered
			    if verbose:
		    		print "Command does not exist"
		try: # Try to reply to the comment
                    c.reply(head + fixed + tail)
		except praw.exception.APIException:
		    if verbose:
			print "Pausing for 2 mins" # RATELIMIT time
		    time.sleep(120)
		    c.reply(head + fixed + tail)
                with open("commented.txt", "a") as myfile:
                    myfile.write("\n" + c.id) # So we know not to message again

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
        return True
    else:
	if verbose:
		print "I have already answered"
        return False
for c in subreddit.stream.comments():
    do_work(c)
