## Notes


# Url to connect tht bot to a server: https://discordapp.com/oauth2/authorize?&client_id=170493165214629888&scope=bot
# id 129340698871726080

# Basic informations. To change if you want to setup your own Bot.
__program__ = "DLBot"
__version__ = "0.0.3a"

## Libaries import

# Testing Initial import
import sys
try:
    assert sys.version_info >= (3, 5)
    from discord.ext import commands
    import discord
except ImportError:
    print("Discord.py is not installed.\n"
          "Consult the guide for your operating system "
          "and do ALL the steps in order.\n")
    sys.exit()
except AssertionError:
    print("Red needs Python 3.5 or superior.\n"
          "Consult the guide for your operating system "
          "and do ALL the steps in order.\n")
    sys.exit()

# Discord imports
import asyncio
import aiohttp
import websockets

# other imports
import requests
import os
import pickle
import datetime
import random
import feedparser
import re


##Variables setup

base = ".."

helptext = """
Here are my commands : 
    -help   : Show this text
    -hello  : Hi !
    -xdy    : Roll some dices ! (ex : 2d100) It will give you x answers between 0 and y
    -galnet : Will give you random GalNet feed unless you specify an index (galnet [i])
    -wiki   : Will give you a wikipedia definition
    -pict   : NOT YET IMPLEMENTED
    -video  : NOT YET IMPLEMENTED

Some commands are not detailed. Good luck finding them !
"""

##Program

# bool isSetUp() : attempts to open setup.txt. Returns true if opening is successful, otherwise returns false.
def isSetUp(file):
    try:
        setupFile=open(file,"r")
        return True
    except:
        return False

# void setup(string language) : sets the bot up at first start. Is only meant to be invoked by setup_common().
def setup(language,pointer):
    if language=="en":
        print("Hello and welcome to DLBot setup assistant. I'll help you setting everything up.")
        print("We need to activate or not some of the functions.")
        quizz=input("Do you want me to enable everything ?").lower()
        if quizz=="y":
            setupArray=["0"]
            setupArray.append("111111")
            print("Everything enabled.")
        elif quizz=="n":
        ##Manual Setup
            print("Manual setup.")
        
            # This stands for the language
            setupArray=["0"]
            
            # Asking the user for each bot function
            quizz=input("Enable videos ? (Y/N) : ").lower()
            if quizz=="y":
                setupArray.append("1")
                print("Quizz     [ON]")
            elif quizz=="n":
                setupArray.append("0")
                print("Quizz     [OFF]")
                
            pics=input("Enable pictures ? (Y/N) : ").lower()
            if pics=="y":
                setupArray.append("1")
                print("Pictures  [ON]")
            elif pics=="n":
                setupArray.append("0")
                print("Pictures  [OFF]")
                
            quotes=input("Enable quotes ? (Y/N) : ").lower()
            if quotes=="y":
                setupArray.append("1")
                print("Quotes    [ON]")
            elif quotes=="n":
                setupArray.append("0")
                print("Quotes    [OFF]")
                
            wiki=input("Enable wiki ? (Y/N) : ").lower()
            if wiki=="y":
                setupArray.append("1")
                print("Wiki      [ON]")
            elif wiki=="n":
                setupArray.append("0")
                print("Wiki      [OFF]")
                
            slog=input("Enable super logging ? (Y/N) : ").lower()
            if slog=="y":
                setupArray.append("1")
                print("S Log     [ON]")
            elif slog=="n":
                setupArray.append("0")
                print("S Log     [OFF]")
            
            # Add the private joke bit - private jokes function can only be activated manually
            setupArray.append("0")
            
        else:
            print("An error occured (bad answer). Please delete setup.txt and restart the bot.\nShutting down...")
            quit()
        
        
        # Write everything in setup.txt
        for i in range(len(setupArray)):
            try:
                pointer.write(setupArray[i])
            except:
                print("An error occured while writing the setup. Current folder might me read-only. Shutting down.")
                pointer.close()
                quit()
        
        print("The bot is correctly set up! You can now start using it!")
        pointer.close()
        return setupArray
    
    elif language=="fr":
        print("Rappelle moi de faire le setup en français aussi.") #TODO: french setup
        setup("en", pointer)

# void setup_common() : starts the setup by asking the language. Redirects to setup() when language is correctly defined.
def setup_common():
    # bool languageOK: defines if the language has been correctly set up
    languageOK=False
    print("setup.txt not found. Creating and entering the setup.")
    try:
        setupFile=open("setup.txt","w")
        print("File created successfully! Please follow the instructions:")
    except:
        print("An error occured. Current folder might me read-only. Shutting down.")
        quit()
    while languageOK==False:
        language=input("Language (FR/EN): ").lower()
        if language=="fr":
            print("Langue sélectionné : Français.")
            languageOK=True
            setup("fr",setupFile)
        elif language=="en":
            print("Language selected : English.")
            languageOK=True
            setup("en",setupFile)
        else:
            print("Invalid language.")
            languageOK=False
            
def start():
    print("setup.txt found. Setup loaded successfully. To reinitialize the setup, simply delete setup.txt.")
    setupFile=open("setup.txt","r")
    setupRead=setupFile.readline()
    setupArray=list(setupRead)
    setupFile.close()
    print(setupArray)
    return setupArray
    
def readToken():
    tokenFile=open("token.txt", "r")
    token = tokenFile.readline()
    tokenFile.close()
    return token
    
def createToken():
    token=input("Please enter you bot's token : ")
    try:
        tokenFile=open("token.txt", "w")
        tokenFile.write(token)
        tokenFile.close()
    except:
        print("An error occured. Shutting down...")
    print("Token registered.")
    
def logMessage(message):
    dir = os.path.dirname("./logs/"+message.server.name+"/")
    if not os.path.exists(dir):
        os.makedirs(dir)
    today = datetime.datetime.now()
    logsFile=open("./logs/" + message.server.name + "/" + str(today.day) + "-" + str(today.month) + "-" + str(today.year) + ".txt","a")
    log = str(today.hour) + ":" + str(today.minute) + ":" + str(today.second) + " [" +  str(message.author.name) + "@" +message.server.name + "." + message.channel.name + "] : " + message.content + "\n"
    logsFile.write(log)
    print(log,end='')
    
def sLogs(message):
    dir = os.path.dirname("./superlogs/"+message.server.name+"/")
    if not os.path.exists(dir):
        os.makedirs(dir)
    today = datetime.datetime.now()
    logsFile=open("./superlogs/" + message.server.name + "/" + str(today.day) + "-" + str(today.month) + "-" + str(today.year) + ".txt","a")
    log = str(today.hour) + ":" + str(today.minute) + ":" + str(today.second) + " [" +  str(message.author.name) + "@" +message.server.name + "." + message.channel.name + "] : " + message.content + "\n"
    logsFile.write(log)

def logStart():
    dir = os.path.dirname("./logs/")
    if not os.path.exists(dir):
        os.makedirs(dir)
    today = datetime.datetime.now()
    logsFile=open("./logs/startup.txt","a")
    log="[" + str(today) + "] : Bot " + __program__ + " v" + __version__ + " logged in as " + client.user.name + " \n"
    logsFile.write(log)
    print(log,end='')
    
def rssFeed(index=None):
    python_wiki_rss_url = "https://community.elitedangerous.com/galnet-rss"
    feed = feedparser.parse( python_wiki_rss_url )
    entries = []
    for i in range(len(feed["items"])):
        if "Weekly" not in feed["items"][i]["title"]:
            entries.append( feed[ "items" ][i] )
    if index == None:
        index = random.randrange(len(entries))
    try:
        return entries[index]
    except:
        return None
    
## Starting the bot!
if isSetUp("setup.txt")==False:
    setup_common()
    setupArray=start()
else:
    setupArray=start()
if isSetUp("token.txt")==False:
    createToken()

    

## The bot itself          
global client
client = discord.Client()

@client.event
@asyncio.coroutine
def on_ready():
    #lel=open("sorataisbored.png","rb")
    #yield from client.edit_profile(avatar=lel.read())
    if setupArray[0]=='0':
        print('Logged in as')
        print(client.user.name)
        print(client.user.id)
        print('------')
    elif setupArray[0]=='1':
        print('Connecté en tant que')
        print(client.user.name)
        print(client.user.id)
        print('------')
    logStart()
    
        
## Other functions

@client.event
@asyncio.coroutine
def Sendmessage(msg,message):
    yield from client.send_message(message.channel, msg)
    logMessage(message)
    


## Starting the coroutines
@client.event
@asyncio.coroutine 
def on_message(message):
    
    # Logs stuff
    today = datetime.datetime.now()
    logsFile=open("./logs/" + str(today.day) + "-" + str(today.month) + "-" + str(today.year) + ".txt","a")
    if (setupArray[5]=="1"):
        sLogs(message)
    
    ## Normal functions
    #TODO: quizz, pic, quote
    
    # Basically a test function
    if message.content.startswith(base+'hello') or ("Hello" in message.content and message.mentions[0].id==client.user.id):
        hellos=["Hello", "Hi", "Hello CMDR", "Greetings", "Welcome", "Oh ! Hi"]
        msg = hellos[random.randrange(len(hellos))] + ' {0.author.mention} !'.format(message)
        yield from client.send_message(message.channel, msg)
        logMessage(message)

    # Still indev
    if message.content.startswith('!pic'):
        msg = '{0.author.mention} Sorry, but !pic is still indev.'.format(message)
        yield from client.send_message(message.channel, msg)
        logMessage(message)
        
    if message.content.startswith('!quizz'):
        msg = '{0.author.mention} Sorry, but !quizz is still indev.'.format(message)
        yield from client.send_message(message.channel, msg)
        logMessage(message)
    
    if message.content.startswith('!quote'):
        msg = '{0.author.mention} Sorry, but !quote is still indev.'.format(message)
        yield from client.send_message(message.channel, msg)
        logMessage(message)
            
    # !wiki
    if message.content.startswith('!wiki') and setupArray[0]=='0':
        messageArray = message.content.split()
        messageArray.remove(messageArray[0])
        toSearch = '_'.join(messageArray)
        msg = ('{0.author.mention} https://en.wikipedia.org/wiki/' + toSearch).format(message)
        yield from client.send_message(message.channel, msg)
        logMessage(message)
    elif message.content.startswith('!wiki') and setupArray[0]=='1':
        messageArray = message.content.split()
        messageArray.remove(messageArray[0])
        toSearch = '_'.join(messageArray)
        msg = ('{0.author.mention} https://fr.wikipedia.org/wiki/' + toSearch).format(message)
        yield from client.send_message(message.channel, msg)
        logMessage(message)
    
    # !help
    if message.content.startswith(base+'help') or ("elp" in message.content.lower() and message.mentions[0].id==client.user.id):
        msg = "{0.author.mention}".format(message) + " Hey ! I'm " + client.user.name + " ! " + helptext
        yield from client.send_message(message.channel, msg)
        logMessage(message)
    
    ## Other functions
    # RSS feed
    if message.content.startswith(base+'galnet'):
        var = message.content.split(" ")
        try :
            var= var[1]
            var = int(float(var))
        except Exception as error:
            print (error)
            var=None
        feed = rssFeed(var)
        if feed == None:
            msg = "No RSS feed loaded. Maybe change the index"
        else:
            msg = "News from GalNet : #" + feed["title"] + "#\n```html\n" + re.sub('<[^<]+?>', '',feed["summary"]) + "```"
        yield from client.send_message(message.channel, msg)
        logMessage(message)
    
    # roll 
    if list(message.content)[0].isdigit() and list(message.content)[1] == "d":
        txt = message.content
        var = txt.split("d")
        msg = "{0.author.mention} rolled ".format(message)+message.content 
        for i in range(int(var[0])):
            msg += "\n It's a "+str(random.randrange(int(var[1]))+1)+" !"
        yield from client.send_message(message.channel, msg)
        logMessage(message)
    
    logsFile.close()
        
try: 
    client.run(readToken())
except:
    print("DLBot not started. There might be a connection error.\nShutting down...")
    quit()