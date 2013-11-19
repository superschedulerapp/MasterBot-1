import BotTalking
import commandant
import pickle
import time
import os

class Data():
    def __init__(self):
        os.chdir('UserData')
        try: file1 = open('ChannelsPickle','r')
        except IOError:
            for item in ['ChannelsPickle','BotsPickle','OwnersPickle','DevsPickle','OpsPickle','FriendsPickle','LinksPickle']:
                os.system('cp ../NewData/'+item+' '+item+'\n')
            file1 = open('ChannelsPickle','r')
        self.Channels = pickle.load(file1)
        file2 = open('BotsPickle','r')
        self.Bots = pickle.load(file2)
        file3 = open('UsersPickle','r')
        self.Users = pickle.load(file3)
        file7 = open('LinksPickle','r')
        self.Links = pickle.load(file7)
        self.Defaults = {}
        os.chdir('..')

Storage = Data()


def Store(Mem = Storage):
    os.chdir('UserData')
    file1 = open('ChannelsPickle','r+')
    pickle.dump(Mem.Channels,file1)
    file1.close()
    file2 = open('BotsPickle','r+')
    pickle.dump(Mem.Bots,file2)
    file2.close()
    file3 = open('UsersPickle','r+')
    pickle.dump(Mem.Users,file3)
    file7 = open('LinksPickle','r+')
    pickle.dump(Mem.Links,file7)
    file7.close()
    os.chdir('..')

def Maintenance(Sock,Storg,Mem =Storage):
    Mem.Bots = {}
    Sock.send('NAMES #chaoscorebots\n')
    line = ''
    while not '/NAMES' in line:
        line = line + Sock.recv(5)
    line2 = line.split()
    print line2
    for item in line2:
        if '[CCB]' in item and not 'MasterBot' in item:
            while item[0] in Storg.US or item[0] == '@':
                item = item[1:]
            if not item in Mem.Bots:
                Mem.Bots[item] = []
    print Mem.Bots
    channeList =Mem.Channels['Master']
    #channeList.pop(channeList.index('#chaoscorebots'))
    if len(Mem.Bots)>=1:
        while len(channeList)>0:
            for item in Mem.Bots:
                try: Mem.Bots[item].append(channeList.pop())
                except IndexError:
                    break
        for item in Mem.Bots:
            map(lambda channel:Sock.send('INVITE '+item+' '+channel+'\n'),Mem.Bots[item])
            Sock.send('PRIVMSG #chaoscorebots :!'+item+' Join '+commandant.l2s(Mem.Bots[item])+'\n')
        time.sleep(10)
        for item in Mem.Channels:
            print Mem.Channels[item]
            if Mem.Channels[item] != '#chaoscorebots':
                Sock.send('NAMES '+Mem.Channels[item]+'\n')
                line = ''
                while not '/NAMES' in line:
                    line = line + Sock.recv(5)
                line2 = line.split()
                print line2
                for thing in line2:
                    while thing[0] in Storg.US or thing[0] == '@':
                        thing = thing[1:]
                    if '!' in thing:
                        break
                    print thing
                    if thing in Mem.Bots:
                         if not Mem.Channels[item] in Mem.Bots[thing]:
                            Sock.send('PRIVMSG #chaoscorebots :!'+thing+' Leave '+Mem.Channels[item]+'\n')
