## Notes


# Url to connect tht bot to a server: https://discordapp.com/oauth2/authorize?&client_id=170493165214629888&scope=bot
# id 129340698871726080

# Basic informations. To change if you want to setup your own HugBot.
__program__ = "DLBot"
__version__ = "0.0.2"

## Libaries import

# Discord stuff
import discord
import asyncio
import aiohttp
import websockets
import datetime

# dbdl3 stuff
import requests
import sys
import os
import pickle

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

##Variables setup

base = ".."

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
        print("Hello and welcome to neiDiscordBot setup assistant! I will help you setting everything up correctly.")
        print("First, let's enable or disable the functions available for the bot.")
        print("To get a list of the available functions with their description, go to https://github.com/neistuff/neiDiscordBot/ and read the README.")
        
        
        # This stands for the language
        setupArray=["0"]
        
        # Asking the user for each bot function
        quizz=input("Enable videos ? (Y/N) : ").lower()
        if quizz=="y":
            setupArray.append("1")
            print("Quizz enabled.")
        elif quizz=="n":
            setupArray.append("0")
            print("Quizz disabled.")
            
        pics=input("Enable pictures ? (Y/N) : ").lower()
        if pics=="y":
            setupArray.append("1")
            print("Pictures enabled.")
        elif pics=="n":
            setupArray.append("0")
            print("Pictures disabled.")
            
        quotes=input("Enable quotes ? (Y/N) : ").lower()
        if quotes=="y":
            setupArray.append("1")
            print("Quotes enabled.")
        elif quotes=="n":
            setupArray.append("0")
            print("Quotes disabled.")
            
        wiki=input("Enable wiki ? (Y/N) : ").lower()
        if wiki=="y":
            setupArray.append("1")
            print("Wiki enabled.")
        elif wiki=="n":
            setupArray.append("0")
            print("Wiki disabled.")
        
        # Add the private joke bit - private jokes function can only be activated manually
        setupArray.append("0")
        
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
        print("An error occured. Shutting down.")
    print("Token registered.")
    
def logMessage(message):
    dir = os.path.dirname("./logs/")
    if not os.path.exists(dir):
        os.makedirs(dir)
    today = datetime.datetime.now()
    logsFile=open("./logs/" + str(today.day) + "-" + str(today.month) + "-" + str(today.year) + ".txt","a")
    log = str(today.hour) + ":" + str(today.minute) + ":" + str(today.second) + " [" +  str(message.author.name) + "@" +message.server.name + "." + message.channel.name + "] : " + message.content + "\n"
    logsFile.write(log)
    print(log,end='')

def logStart():
    dir = os.path.dirname("./logs/")
    if not os.path.exists(dir):
        os.makedirs(dir)
    today = datetime.datetime.now()
    logsFile=open("./logs/" + str(today.day) + "-" + str(today.month) + "-" + str(today.year) + ".txt","a")
    log="[" + str(today) + "] : Bot " + client.user.name + " logged in ! \n"
    logsFile.write(log)
    #print(log,end='')
    
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
    elif setupArray[1]=='1':
        print('Connecté en tant que')
        print(client.user.name)
        print(client.user.id)
        print('------')
    logStart()
        
## Other functions



## Starting the coroutines
@client.event
@asyncio.coroutine 
def on_message(message):
    
    # Logs stuff
    today = datetime.datetime.now()
    logsFile=open("./logs/" + str(today.day) + "-" + str(today.month) + "-" + str(today.year) + ".txt","a")
    
    ## Normal functions
    #TODO: quizz, pic, quote
    
    # Basically a test function
    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}!'.format(message)
        yield from client.send_message(message.channel, msg)
        log="Answered hello to " + str(message.author) + " on channel #" + message.channel.name + " at " + str(today) + "\n"
        logsFile.write(log)
        print(log,end='')
    
    # Still indev
    if message.content.startswith('!pic'):
        msg = '{0.author.mention} Sorry, but !pic is still indev.'.format(message)
        yield from client.send_message(message.channel, msg)
        log="Answered !pic to " + str(message.author) + " on channel #" + message.channel.name + " at " + str(today) + "\n"
        logsFile.write(log)
        print(log,end='')
        
    if message.content.startswith('!quizz'):
        msg = '{0.author.mention} Sorry, but !quizz is still indev.'.format(message)
        yield from client.send_message(message.channel, msg)
        log="Answered !quizz to " + str(message.author) + " on channel #" + message.channel.name + " at " + str(today) + "\n"
        logsFile.write(log)
        print(log,end='')
    
    if message.content.startswith('!quote'):
        msg = '{0.author.mention} Sorry, but !quote is still indev.'.format(message)
        yield from client.send_message(message.channel, msg)
        log="Answered !quote to " + str(message.author) + " on channel #" + message.channel.name + " at " + str(today) + "\n"
        logsFile.write(log)
        print(log,end='')
            
    # !wiki
    if message.content.startswith('!wiki') and setupArray[0]=='0':
        messageArray = message.content.split()
        messageArray.remove(messageArray[0])
        toSearch = '_'.join(messageArray)
        msg = ('{0.author.mention} https://en.wikipedia.org/wiki/' + toSearch).format(message)
        yield from client.send_message(message.channel, msg)
        log="Answered !wiki to " + str(message.author) + " on channel #" + message.channel.name + " at " + str(today) + "\n"
        logsFile.write(log)
        print(log,end='')
    elif message.content.startswith('!wiki') and setupArray[0]=='1':
        messageArray = message.content.split()
        messageArray.remove(messageArray[0])
        toSearch = '_'.join(messageArray)
        msg = ('{0.author.mention} https://fr.wikipedia.org/wiki/' + toSearch).format(message)
        yield from client.send_message(message.channel, msg)
        log="!wiki répondu à " + str(message.author) + " dans le channel #" + message.channel.name + " à " + str(today) + "\n"
        logsFile.write(log)
        print(log,end='')
    
    # !help
    if message.content.startswith(base+'help'):
        msg = "{0.author.mention}".format(message) + " Hey ! I'm " + client.user.name + " ! Command list is not ready yet."
        yield from client.send_message(message.channel, msg)
        logMessage(message)
    
    ## Other functions
    

    
    logsFile.close()
        
client.run(readToken())
