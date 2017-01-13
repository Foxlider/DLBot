## Notes


# Url to connect tht bot to a server: https://discordapp.com/oauth2/authorize?&client_id=170493165214629888&scope=bot
# id 129340698871726080

# Basic informations. To change if you want to setup your own Bot.
__program__ = "DLBot"
__version__ = "0.1.7a"

## Libaries import

# Testing Initial import
import sys
try:
    assert sys.version_info >= (3, 4)
    from discord.ext import commands
    import discord
except ImportError:
    print("Discord.py is not installed.\n"
          "Consult the guide for your operating system "
          "and do ALL the steps in order.\n")
    sys.exit()
except AssertionError:
    print("DLBot needs Python 3.4 or superior.\n"
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

import setup


##Variables setup
#BASE STRING : change it if you want, I don't care
base = ".."

#Message sent when the user call for help
helptext = """
Here are my commands : 
    -help   : Show this text. Use help aCommand to get the command definition
    -hello  : Hi !
    -xdy    : Roll some dices ! (ex : 2d100) It will give you x answers between 0 and y
    -galnet : Will give you random GalNet feed unless you specify an index (galnet [i])
    -wiki   : Will give you a wikipedia definition
    -pict   : NOT YET IMPLEMENTED
    -yt     : Put some videos in your channel !
    -quote  : When funny things are said, you must save them !

Some commands are not detailed. Good luck finding them !
"""
#List of my functions
functions=['help', 'hello', 'xdy', 'galnet', 'wiki', 'pict', 'yt', 'quote']

#WTF IS THAT ? That's the documentation dictionary ! 
helpdict = dict(help=base+"""help [command|all] : 
Why are you wanting help on help anyway ?
    command : function handled by the bot
    all     : if you wan all the documentation"""
                , hello=base+"""hello
Hello @DLBot : 
It will say Hello. That's all !"""
                , xdy="""{x}d{y} : 
Used in roleplay games. Like rolling 1 dice containing 20 faces will be 1d20
    x : number between 1 and 10
    y : number greater than 1"""
                , galnet=base+"""galnet [index] : 
Used to get RSS feed from GalNet forums. Use the index to see a specific news or let it be random
    index : number of the news wanted"""
                , wiki=base+"""wiki [word] : 
When you are too lazy to surf on the internet by yourself."""
                , pict="Kill me please... Don't you read the help ? Oh..."
                , yt = base+"""yt [-s|-p] [link|index] [title] : 
Youtube function to have some videos on the channel !
    -s    : Option to save the link (need the link in the command line)
    -p    : Will play the selected video
    link  : link to a YouTube video
    index : index of a saved link
    title : title of the saved link (need the -s option)"""
                , quote=base+"""quote [s] [quote|index] : 
Used to quote your friends when they are funny or to remember a funny quote
    -s : Used to save a quote (need the quote in the command line)
    quote : quote that will be saved
    index : index of a saved quote""")

global datadir
datadir = os.path.dirname("./data/")
if not os.path.exists(datadir):
    os.makedirs(datadir)
    

##Program

# bool isSetUp() : attempts to open setup.txt. Returns true if opening is successful, otherwise returns false.
def isSetUp(file):
    try:
        setupFile=open(file,"r")
        return True
    except:
        return False



def readToken():
    tokenFile=open(datadir+"/token.txt", "r")
    token = tokenFile.readline()
    tokenFile.close()
    return token
    
def createToken():
    token=input("Please enter you bot's token : ")
    try:
        tokenFile=open(datadir+"/token.txt", "w")
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
        
def ytSave(link, title):
    ytFile = open (datadir+"/yt.txt", "a")
    ytFile.write(title + " " + link + "\n")
    print("Saved link "+ link)
    ytFile.close()
    return "Saved link n°"+ str(fileSize(datadir+"/yt.txt")) 
    
def ytRead(pos):
    ytFile = open(datadir+"/yt.txt" , "r")
    ytList = ytFile.readlines()[int(pos)-1].strip("\n")
    #print (ytList)
    ytFile.close()
    return ytList
    
def ytPlay(target):
    if target.isdigit():
        print('Playing video from list : ' + target + ' +link')
        msg = 'Playing video from list : ' + target + '\n'
        ytlink = ytRead(target)
        msg += ytlink.split(' ')[1]
        print(ytlink.split(' ')[1])
    else:
        msg = 'Playing video from YouTubeApi : ' + target
        print('Playing video from YouTubeApi : ' + target)
    return msg
        
def qtSave(quote):
    qtFile = open (datadir+"/quote.txt", "a")
    qtFile.write(quote + "\n")
    print("Saved quote "+ quote)
    qtFile.close()
    return "Saved quote n°"+ str(fileSize(datadir+"/quote.txt")) + " : " + quote

def qtRead(index):
    qtFile = open(datadir+"/quote.txt" , "r")
    qtList = qtFile.readlines()[int(index)-1].strip("\n")
    qtFile.close()
    return qtList
    
def fileSize(filename):
    file = open(filename, 'r')
    num = len(file.readlines())
    file.close()
    return num
    
## Starting the bot!
if isSetUp(datadir+"/setup.txt")==False:
    setup.setup_common()
    setupArray=setup.start()
else:
    setupArray=setup.start()
if isSetUp(datadir+"/token.txt")==False:
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
    lowerContent = message.content.lower
    
    ## Normal functions
    #TODO: quizz, pic, quote
    
    ## A test function
    if message.content.startswith(base+'hello') or ("Hello" in message.content and message.mentions[0].id==client.user.id):
        hellos=["Hello", "Hi", "Hello CMDR", "Greetings", "Welcome", "Oh ! Hi"]
        msg = hellos[random.randrange(len(hellos))] + ' {0.author.mention} !'.format(message)
        yield from client.send_message(message.channel, msg)
        logMessage(message)
        
    ## Another test function
    if message.content.startswith(base+'version'):
        msg = __program__ + ' is version v' + __version__ + '. '
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
            
    ## Wiki
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
    
    ## Help Function
    if message.content.startswith(base+'help') or (lowerContent.startswith("help") and message.mentions[0].id==client.user.id):
        msg = "{0.author.mention}".format(message) + " Hey ! I'm " + client.user.name + " ! " + helptext
        
        args = message.content.split(" ")
        try:
            if args[1] in functions:
                msg = 'Usage : \n' + helpdict[args[1]]
            elif args[1]=='all':
                msg = 'All the definitions : \n'
                for defs in functions:
                    msg += '```\n' + helpdict[defs] + '```\n'
            else:
                msg = "WTF is this function ?\n"+str(functions)+" that's all I have !"
        except IndexError:
            msg = "{0.author.mention}".format(message) + " Hey ! I'm " + client.user.name + " ! " + helptext
        yield from client.send_message(message.channel, msg)
        logMessage(message)
    
    # Other functions
    ## RSS feed
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
    
    ## Roll 
    if list(message.content)[0].isdigit() and list(message.content)[1] == "d":
        txt = message.content
        var = txt.split("d")
        msg = "{0.author.mention} rolled ".format(message)+message.content 
        for i in range(int(var[0])):
            msg += "\n It's a "+str(random.randrange(int(var[1]))+1)+" !"
        yield from client.send_message(message.channel, msg)
        logMessage(message)
     
    ## Quote Function
    if message.content.startswith(base+'quote'):
        mess = message.content.strip()
        args = mess.split()
        #Wanna read a quote ?
        if len(args)>=2:
            if args[1].isdigit():
                msg = 'Reading quote...\n'
                try:
                    msg += qtRead(args[1]) + "\n"
                except:
                    msg += 'No quote found. Maybe the index was too big'
            #Or better ! A random quote !
            elif args[1] == '-r':
                msg = qtRead(random.randrange(fileSize(datadir+'/quote.txt')))
            #Or wanna save one ?
            else:
                print('Saving quote')
                msg = qtSave(mess.strip(base + 'quote '))
        else:
            print('No index specified')
            msg = qtRead(random.randrange(fileSize(datadir+'/quote.txt')))
        yield from client.send_message(message.channel, msg)
        logMessage(message)
       
    ## Youtube Function
    if message.content.startswith(base+'yt'):
        mess = message.content.strip()
        args = mess.split(" ")
        #If the function have a link
        if 'youtu' in mess:
            #Wanna save ?
            if args[1] == '-s':
                try:
                    msg = ytSave(args[2], args[3])
                except:
                    msg = ytSave(args[2], "NoTitle")
            #Wanna play ?
            elif args[1] == '-p':
                msg = "Playing video " + args[2] + "\n"
                msg += ytPlay(args[2])
            #Or just want some informations about it ?
            else:
                msg =  "Finding vidéo " + args[1] + " Oh wait... I can't yet... Sorry !"
        #No link ?
        else:
            #Want to search in the file ?
            if len(args) >= 2:
                if args[1].isdigit():
                    try:
                        msg = ytRead(args[1])
                    except:
                        msg = "No link found"
                # Maybe search for an onlie video ?
                elif args[1].isalnum():
                    msg= "Research video online : " + args[1] + " But I can't do that yet... Sorry ! "
                
                #Hum... Play from file ?
                elif args[1] == '-p' and args[2].isdigit():
                    msg = "Playing video " + args[2] + '\n'
                    msg += ytPlay(args[2])
                #"Something bad happend... Something very bad...
                else:
                    print("error")
                    msg = "Something happend. I'm sure something happend. But dunno what. Sorry !"
            else:
                print('No index specified')
                msg = ytRead(random.randrange(fileSize(datadir+'/yt.txt')))
        yield from client.send_message(message.channel, msg)
        logMessage(message)
        
        
    
    logsFile.close()
        
try: 
    client.run(readToken())
except:
    print("DLBot not started. There might be a connection error.\nShutting down...")
    quit()
