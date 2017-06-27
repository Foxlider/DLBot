import os
from collections import *

##Variables setup
global setupdict  
setupdict = OrderedDict(videos='[OFF]'
                ,pictures='[OFF]'
                ,quotes='[OFF]'
                ,wiki='[OFF]'
                ,SLogs='[OFF]'
                ,pvj = '[OFF]')
                
                
                
d = OrderedDict(This='oh',is_a='my',test='god')
for key in d:
    print(key)

setupkeys=['videos  ','pictures','quotes  ','wiki    ','SLogs   ','pvj     ']
global datadir
datadir = os.path.dirname("./data/")
if not os.path.exists(datadir):
    os.makedirs(datadir)

# void setup(string language) : sets the bot up at first start. Is only meant to be invoked by setup_common().
def setup(language,pointer):
    if language=="en":
        print("Hello and welcome to DLBot setup assistant. I'll help you setting everything up.")
        print("We need to activate or not some of the functions.")
        quizz=input("Do you want me to enable everything ? (y/n)").lower()
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
        setupFile=open(datadir+"/setup.txt","w")
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
    setupFile=open(datadir+"/setup.txt","r")
    setupRead=setupFile.readline()
    setupArray=list(setupRead)
    setupFile.close()
    #print(setupArray)
    i=1
    for set in setupkeys:
        if setupArray[i] == '1':
            setupdict[set.strip()] = '[ON]'
        else:
            setupdict[set.strip()] = '[OFF]'
        print(set + '  ' + setupdict[set.strip()])
        i+=1
        
    return setupArray
    
    

    
    
    
