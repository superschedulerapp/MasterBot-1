import os

#Only used the first time the script is run. If /userData doesn't exist,
#create it and populate it with dummy data from /newData

def initData():
    if not os.path.isdir('./UserData/'):
        os.mkdir('./UserData/')
    if not os.path.isfile('./UserData/Data.txt'):
        for item in ['ChannelsPickle','UsersPickle','BotsPickle','LoginInfoPickle','LinksPickle','Data.txt']:
            os.system('cp ./NewData/'+item+' ./UserData'+item+'\n')
