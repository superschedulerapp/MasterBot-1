import os

def initData():
    if not os.path.isdir('./UserData/'):
        os.mkdir('./UserData/')
    if not os.path.isfile('./UserData/Data.txt'):
        for item in ['ChannelsPickle','UsersPickle','BotsPickle','LoginInfoPickle','LinksPickle','Data.txt']:
            os.system('cp ../NewData/'+item+' '+item+'\n')
