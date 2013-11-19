import random
import MasterBotter
import zipIt
import os
import HighScores

HStypes = {0:'Total',1:'Economy',2:'Research',3:'Military',5:'Military Built'
                    ,6:'Military Destroyed',4:'Military Lost',7:'Honor'}

for key in HStypes.keys():
    HStypes[HStypes[key]] = key

def l2s(listy):
    '''
    Convert a List of strings into one string.
    '''
    stria = ''
    if type(listy) == type([]):
        for item in listy:
            if '\\\\' in item:
                pos = item.index('\\\\')
                item = item[:pos] + item[pos+1:]
            stria = stria +(' 'if (stria != ''  and item != '' )else '')+item
        return stria
    else:return listy

def l2t(listy):
    '''
    Converts a list of integers (potentially in string form) into a tuple
    '''
    Tup =  (int(listy[0]),)
    for item in listy[1:]:
        Tup = Tup + (int(item),)
    return Tup

def d2t(dicty):
    '''
    Converts a dictionary into a list of tuples
    '''
    rList = []
    for key in dicty:
        rList.append((key,dicty[key]))
    return rList

class Mem():
    '''
    Memory class for command dictionaries
    '''
    def __init__(self):
        '''
        Where most of the command parsing work is done.
        '''

        ##initialize a few dictionaries and load the file
        self.cmds = {}
        self.CTypes = {}
        self.Helps = {1:[],2:[],3:[]}
        self.fillers = {}
        self.Permissions = {}
        file1 = open('./Code/Commands.txt','r')

        ##The Following Parses the command file.
        ##Commands should occupy 1 line, and be of the following form:
        ##!Command ::# options
        ##
        ## ::# is the identifier for different sections of the command
        ## ::0 is a string to be sent to IRC
        ## ::1 is for python code, primarily to assign 'fillers' list
        ##      however this can be used for other actions if needed.
        ##      Assigning 'fillers' is usually mandatory.
        ##      The basic principle to live by is, Make sure *ditem in
        ##      the main command function will perform it's duties.
        ## ::8 is Permissions and command types
        ##      The first number is Permission level,0-99 for the command itself
        ##      The second number is Identification needed
        ##          1 is no ID needed
        ##          2 is login needed
        ##          3 is sufficient permissions required.
        ##      The third number is the Help dictionary.
        ##          1 is regular commands (command "Help")
        ##          2 is errors
        ##          3 is DevHelp
        ## ::9 is a tuple to be returned to BotShell.py
        ##      The best description of their use can be found
        ##      in the commands !Reload, !Reboot, !Reconnect, and !Quit

        for line in file1:
            if line[0] == '!':
                line2 = line.split()
                trigger0,trigger1,trigger8,trigger9 = False,False,False,False
                Placements = []
                Command = line2[0][1:].lower()
                for item in line2:
                    if item == '::0':
                        trigger0 = True
                        Placements.append(line2.index(item))
                    if item == '::1':
                        trigger1 = True
                        Placements.append(line2.index(item))
                    if item == '::8':
                        trigger8 = True
                        Placements.append(line2.index(item))
                    if item == '::9':
                        trigger9 = True
                        Placements.append(line2.index(item))
                self.cmds[Command] = {}
                counter = 0
                if trigger0:
                    if trigger1 or trigger8 or trigger9: ender = Placements[1]
                    else: ender = None
                    self.cmds[Command][0] = 'CommandString = "'+l2s(line2[Placements[counter]+1:ender])+'"'
                    counter += 1
                if trigger1:
                    if trigger8 or trigger9: ender = Placements[counter+1]
                    else: ender = None
                    self.cmds[Command][1] = l2s(line2[Placements[counter]+1:ender])
                    counter += 1
                if trigger8:
                    if trigger9: ender = Placements[counter+1]
                    else: ender = None
                    datas = line2[Placements[counter]+1:ender]
                    self.Permissions[Command] = int(datas[0])
                    self.CTypes[Command] = l2t(datas[1:])
                    self.Helps[self.CTypes[Command][1]].append(Command)
                    counter += 1
                if trigger9:
                    self.cmds[Command][9] = l2t(line2[Placements[-1]+1:])

        ##Unused? previously intended as a channels dictionary.
        ##MasterBotter has that role currently.
        self.CN = {}    

        ##Leading commands on server message
        self.Cmd = {0:'PRIVMSG',1:'MODE',2:'INVITE',3:'NOTIFY'
                   ,4:'PART',5:'JOIN',6:'KICK',7:'\x01ACTION',8:'\x01'}

        ##Error messages. Also not Used. Errors show up in Commands
        self.CTErr = {0:"I'm sorry "}   

Memo = Mem()

def parse(line,s,Memory = Memo):
    '''
    Designed for parsing a received line which has a :! in it
    and returning most of the variables used in filling
    '''
    User,ID,Command,Target,Bot,ChannelTarget,Extras = (None for _ in range(7))
    Channel = line[2]
    Target,ChannelTarget = [],[]
    name = line.pop(0)    
    if '!~' in name:
        spot = name.index('!~')
        User =name[1:spot]
        ID =  name[spot+2:]
    elif '!' in name:
        spot = name.index('!')
        User =name[1:spot]
        ID =  name[spot+1:]
    for item in line:
        if ':!' in item:
            if Bot == None:
                Bot = item[2:]
                indy = line.index(item)
                try: Command = line[indy+1].lower()
                except IndexError:
                    Command = 'cam'
                    break
        if '@' in item and item[1] != '#' and Command != None and not item[1:] in Target:
            if item[-1] == ',':
                item = item[:-1]
            if item[1:] in MasterBotter.Storage.Channels:
                ChannelTarget = ChannelTarget + MasterBotter.Storage.Channels[item[1:]]
            else:
                Target.append(item[1:])
        if '@#' in item and Command != None and not item[1:] in ChannelTarget:
            if item[-1] == ',':
                item = item[:-1]
            ChannelTarget.append(item[1:])
        if '^' in item and Command != None:
            try: PNew = MasterBotter.Storage.Users[item[1:]]
            except: PNew = 0
            try: PMine = MasterBotter.Storage.Users[User]
            except: PMine = 0
            if PMine >= PNew:
                User = item[1:]
        if '::' in item:
            breaky = line.index(item)
            Extras = line[breaky:]
            Extras[0] = Extras[0][2:]
            if Extras[0] == '':
                try: Extras = Extras[1:]
                except IndexError:
                    Extras = []
                    break
            if Extras == []:
                break
            if Extras[0][0] == ':':
                Extras[0] = Extras[0][1:]
                Extras = l2s(Extras)
            break
    if ChannelTarget != None and Target == []:
        for item in ChannelTarget:
            Target.append(item)
    if Target == []:
        Target = User
    if ChannelTarget != []:
        Channel = ChannelTarget
    if Channel == s.CI['NICK']:
        Channel = User
    return User,Bot,ID,Command,Channel,Target,Extras

def PermFilter(User,ID,Command,S,Memory = Memo):
    '''
    Takes the User, ID, and Command, and compares to stored info 
        to see if this User is allowed to execute the given command.
    '''
    try: CType = Memory.CTypes[Command][0]
    except KeyError:
        return False, 'err1'
    if User == S.CI['OWNER']:
        permission = 99
    else:        
        try: permission = MasterBotter.Storage.Users[User]
        except KeyError:
            permission = 0
    try: checkID = MasterBotter.Storage.LoggedInfo[User]
    except KeyError:
        checkID = 0
    if CType == 1:
        return True, Command
    if ID != checkID and CType in [2,3]:
        return False, 'err2'
    if permission < Memory.Permissions[Command] and CType == 3:
        return False, 'err3'
    return True, Command

def reFill(fillers,M):
    '''
    Recursively define a list of lists,
    where the interior lists are every combination of
    the lists of values in fillers, should there be any.
    Meaning, if you have three values in a list for targets,
    lister will contain 3 lists with identical values
    except for the 3 different targets.
    Recursion provides support for lists in multiple positions.
    '''
    lister = []
    if type(fillers[0]) == type(1):fillers[0] = M.Cmd[fillers[0]]
    for item in fillers:
        indy = fillers.index(item)
        if type(item) is list:
            for subitem in item:
                subfill = fillers[:indy] + [subitem]+ fillers[indy+1:]
                for itemize in subfill[indy:]:
                    if type(itemize) is type([]) or type(itemize) is type((x for x in [1])):
                        addedlist = reFill(subfill,M)
                        break
                else:
                    lister.append(subfill)
                    continue
                for Litem in addedlist:
                    lister.append(Litem)
            break
    else:
        lister = [fillers]
    return lister

def commands(line,socket,storage):
    '''
    Receives the split line (List form) from Runcode.
    Returns a string which will either be passed to IRC or returned to shell script.
    '''
    global User, M, Bot, ID, Command,Channel,Target,Extras,MasterBotter
    M = Memo
    User,Bot,ID,Command,Channel,Target,Extras = parse(line,storage)
    if Bot in storage.CI['RespondTo']:
        Test,Command = PermFilter(User,ID,Command,storage)
        f = open('UserData/Log.txt','r+')
        f.readlines()
        f.write(l2s(line))
        f.close()
        SendingDict = {}
        exec M.cmds[Command][0]
        try: exec M.cmds[Command][1]
        except:
            print "Command failed!"
            return {0:['PRIVMSG '+User+ ' :Please give me the proper options to '
                       'use by typing ::{options} at the end of the command!!']}
        SendingDict[0] = []
        FullFilled = reFill(fillers,M)
        for ditem in FullFilled:
            SendingDict[0].append(CommandString.format(*ditem))
        try: SendingDict[9] = M.cmds[Command][9]
        except KeyError:
            pass
        print SendingDict
        return SendingDict
    else:
        print "I'm not",Bot
        return {9:(1,2)}
