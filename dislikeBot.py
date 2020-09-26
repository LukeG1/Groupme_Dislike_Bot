from groupy import attachments
from groupy import Client
import shakesperescraper
import showLetter
import random
import time
import sys

#Set some global varriables
group = ""
groupClient = ""
sigChar = ""
botID = ""
quitFlag = False

#set the group
def setGroup(name):
    global group, groupClient
    groupClient = Client.from_token("----GROUPME_API_TOKEN----")
    groups = list(groupClient.groups.list_all())
    for x in groups:
        if(str(x.name) == name):
            group = x

#initalize the bot and group
def startUp(groupName,botID2,sigChar2):
    global botID, sigChar
    setGroup(groupName)
    botID = botID2
    sigChar = sigChar2

#check if a command with a person has been called
def command(msg,title):
    if(msg[0]==sigChar and msg[1:len(title)+1]==title and msg[len(title)+2]=="@"):
        return str(msg[msg.index("@")+1:])
    return False

#check if a command without a person has been called
def commandBasic(msg,title):
    if(msg[0]==sigChar and msg[1:len(title)+1]==title):
        return True
    return False

#check if a command that has extra info has been called
def commandUse(msg,title):
    if(msg[0]==sigChar and msg[1:len(title)+1]==title):
        return msg[len(title)+1:].strip()
    return False

#find someones last message given their name
def findLastMsg(name):
    if(len(name)>1):
        for message2 in group.messages.list_all():
            if(str(message2.name.lower())==name.strip()):
                return message2.text
    return False
                
def check():
    #bring in the global varriables
    global group, groupClient, quitFlag

    #initilaze basic data
    for m in group.messages.list_all():
        message = m
        break
    msg = str(message.text).lower()
    sender = str(message.name)

    #if the message is deemed legitimate 
    if(len(msg)>2):

        #cancel the program in case of emergency
        commandTest = commandBasic(msg,"exit")
        if(commandTest and sender == "Luke Gabel"):
            group._bots.post(botID,"Dislike bot has been disabled!")
            quitFlag = True
            sys.exit()

        #return someones last message disliked
        person = command(msg,"dislike")
        if(person != False):
            tempMsg = findLastMsg(person)
            if(tempMsg != False):
                group._bots.post(botID,str(sender)+" disliked \" "+str(tempMsg)+" \"")
        
        #return someones most recent message in random case
        person = command(msg,"sarcasm")
        if(person != False):
            tempMsg = findLastMsg(person)
            if(tempMsg != False):
                group._bots.post(botID,"\" "+''.join(random.choice((str.upper,str.lower))(x) for x in tempMsg)+" \"")

        #retrun a picture of the ice age baby
        commandTest = commandBasic(msg,"iceagebaby")
        if(commandTest):
            with open('C:\\Users\\lmgab\\PycharmProjects\\tensorenv\\Random\\iceagebaby.png', 'rb') as f:
                group._bots.post(botID,groupClient.images.from_file(f).url)

        #return a shakespereian insult
        person = command(msg,"shakespere")
        if(person != False):
            group._bots.post(botID,shakesperescraper.getInsult(person))

        #return given text in andrews handwriting
        text = commandUse(str(message.text),"andyfiy")
        if(text != False and len(text)>2):
            showLetter.draw("\n"+text+"\n","TESTAUTOCROP")
            with open("C:\\Users\\lmgab\\PycharmProjects\\tensorenv\\handwriting\\mostRecent.png", 'rb') as f:
                image = groupClient.images.from_file(f)
            group._bots.post(botID,image.url)

        #run the code sent
        code = commandUse(str(message.text),"execute")
        if(code != False):
            if(sender == "Luke Gabel"):
                code = "def thing():\n    "+str(code).replace(";","\n    ")+"\ngroup._bots.post(botID,str(thing()))"
                try:
                    exec(code)     
                except:
                    group._bots.post(botID,"That code couldn't be run due to " + str(sys.exc_info()[0]))
            else:
                group._bots.post(botID,"Only Luke Gabel can run code")

#run the start function in a try loop to avoid timeout errors
notStarted = True
while(notStarted):
    try:
        startUp(
            groupName = "GROUPNAME",
            botID2 = "BOT_ID",
            sigChar2 = "!" #SIGNAL
        )

        group._bots.post(botID,"Dislike Bot is active!\n\nCurrent Commands:\n/dislike\n/sarcasm\n/andyfiy\n/iceagebaby")
        print("Started!")
        notStarted = False
    except:
        print("Couldnt start!")
        notStarted = True
        time.sleep(5)

c = 0
while True:
    try:
        check()
        time.sleep(1)
    except:
        if(quitFlag):
            sys.exit()
        time.sleep(10)
    print(c,end = "\r")
    c+=1
