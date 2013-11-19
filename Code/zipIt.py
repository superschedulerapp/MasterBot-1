import os
import time
import subprocess

def NUB():
    pass

def zipit():
    os.chdir('..')
    botname = "MasterBotCode"
    # Better not pollute the code directory.
    lastupfile = "/tmp/lastircbotuploadtime"
    lasttime = 0
    uploadpath = ""

    if os.path.isfile(lastupfile):
        f = open(lastupfile)
        lasttime = int(f.readline())
        print lasttime
        # In case we don't need to update the archive
        uploadpath = f.readline()
        f.close()

    # Last update time of the bot.
    updatetime = int(os.path.getmtime('./MasterBot/'))
    print updatetime
    
    #Creation of the archive.
    if lasttime < updatetime:
    # I like BASH... or maybe I am just lazy.
        try:os.remove('./MasterBotCode.zip')
        except:pass
        os.system('zip -r ./' + botname + ".zip ./MasterBot/Code")
        os.system("zip -r ./" + botname + ".zip ./MasterBot/NewData")
        os.system('zip ./'+botname+ '.zip ./MasterBot/BotShell.py')
        uploadpath = subprocess.check_output("curl -s -L www.filebin.ca/upload.php -F file=@./" + botname +  ".zip", shell=True).splitlines()[1][4:]
        f = open(lastupfile, "w+")
        f.write(str(updatetime) + "\n" + uploadpath + "\n")
        f.close()

    # This is where you
    # return the message
    os.chdir('MasterBot')
    return uploadpath
