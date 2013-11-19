import BotTalking
import pickle
import time
import os

class Data():
    '''Where a goodly portion of the data that the bot uses to connect to where
    it needs to be is contained, as well as methods for dealing with the data.'''
    def __init__(self):
        '''Load known data.'''
        os.chdir('UserData')
        try: file1 = open('ChannelsPickle','r')
        except IOError:
            for item in ['ChannelsPickle','UsersPickle','BotsPickle','LoginInfoPickle','LinksPickle','PermLoggedInfoPickle','Log.txt']:
                os.system('cp ../NewData/'+item+' '+item+'\n')
            file1 = open('ChannelsPickle','r')
        self.Channels = pickle.load(file1)
        file2 = open('BotsPickle','r')
        self.Bots = pickle.load(file2)
        file3 = open('UsersPickle','r')
        self.Users = pickle.load(file3)
        file4 = open('LoginInfoPickle','r')
        self.LoginInfo = pickle.load(file4)
        file5 = open('PermLoggedInfoPickle','r')
        self.PermLoggedInfo = pickle.load(file5)
        self.LoggedInfo = self.PermLoggedInfo
        file7 = open('LinksPickle','r')
        self.Links = pickle.load(file7)
        self.Defaults = {}
        os.chdir('..')

    def isIndex(self,IndexList,test = 0):
        newList = []
        for item in IndexList:
            if item in self.Channels and test == 0:
                newList.append(item)
            elif not item in self.Channels and test == 1:
                newList.append(item)
        if newList == []:
            newList = ['No indices passed!']
        return newList

    def isChannel(self,Channel,Index):
        return True if Channel in self.Channels[Index] else False

    def AddIndex(self,IndexList):
        for item in IndexList:
            self.Channels[item] = []

    def DelIndex(self,IndexList):
        for item in IndexList:
            try: self.Channels.pop(item)
            except KeyError:
                pass

    def AddChans(self,Chans,IndexList):
        for Chan in Chans:
            for item in IndexList:
                if not self.isChannel(Chan,item):
                    self.Channels[item].append( Chan)

    def DelChans(self,Chans,IndexList):
        for Chan in Chans:
            for item in IndexList:
                if self.isChannel(Chan,item):
                    self.Channels[item].pop(self.Channels[item].index(Chan))

    def DelChanAll(self,Chans):
        for Key in self.Channels:
            newList = []
            for item in self.Channels[Key]:
                if not item in Chans:
                    newList.append(item)
            self.Channels[Key] = newList

Storage = Data()

def Store(Mem = Storage):
    '''Dump known data.'''
    os.chdir('UserData')
    file1 = open('ChannelsPickle','w+')
    pickle.dump(Mem.Channels,file1)
    file1.close()
    file2 = open('BotsPickle','w+')
    pickle.dump(Mem.Bots,file2)
    file2.close()
    file3 = open('UsersPickle','w+')
    pickle.dump(Mem.Users,file3)
    file3.close()
    file4 = open('LoginInfoPickle','w+')
    pickle.dump(Mem.LoginInfo,file4)
    file4.close()
    file5 = open('PermLoggedInfoPickle','w+')
    pickle.dump(Mem.PermLoggedInfo,file5)
    file5.close()
    file7 = open('LinksPickle','w+')
    pickle.dump(Mem.Links,file7)
    file7.close()
    os.chdir('..')

def Maintenance(Sock,Storg,Mem =Storage):
    '''A second attempt at using one bot to control other bots of the same type.'''
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
