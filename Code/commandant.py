import random
import MasterBotter
import zipIt
import os

def l2s(listy):
    '''Doc
    '''
    stria = ''
    for item in listy:
        stria = stria +(' 'if stria != '' else '')+item
    return stria

def chcheck(listy,Channel):
    """
    checking if first listy item is a channel
    """
    if listy[0][0] == '#':
        Channel = listy.pop(0)
    elif listy[0][0] == '@':
        Channel = listy.pop(0)[1:]
    return listy,Channel

class Mem():
    def __init__(self):
        self.cmds = {}
        self.CN = {}
        self.Permissions = {}

def Win(channel,user,listy,*args):
    if len(listy) > 0:
        user = listy[0]
    return 'PRIVMSG ' + channel + " :You're a winner, "+user+"!"

def Kick(channel,user,listy,*args):
    if len(listy) == 0:
        return 'PRIVMSG ' + channel + " :You're a LOSER, "+user+'!\nKICK '+channel+' '+user
    else:
        if listy[0] == '[CCB]MasterBot':
             return 'PRIVMSG '+channel+" :You're a LOSER, "+user+'!\nKICK '+channel+' '+user
        return 'PRIVMSG ' + channel + " :You're a LOSER, "+listy[0]+'!\nKICK '+channel+' '+listy[0]

def Index(channel,user,listy,s,stg,*args):
    stringer = 'PRIVMSG '+channel+' :'+user+', here are the channel indices you requested:\nPRIVMSG '+channel+' :'
    if len(listy) > 0:
        if listy[0] == 'show':
            indices = MasterBotter.Storage.Channels.keys()
            indices.pop(indices.index('Master'))
            return 'PRIVMSG '+channel+' :I know of the following indices: '+l2s(indices)
        if 'a' in listy:
            stringer = stringer + l2s(MasterBotter.Storage.Channels['a'])
        elif 'p' in listy:
            stringer = stringer + l2s(MasterBotter.Storage.Channels['p'])
        if 'h' in listy and MasterBotter.Storage.Users[user] >=70:
            stringer = stringer +' '+ l2s(MasterBotter.Storage.Channels['h'])
        if stringer ==  'PRIVMSG '+channel+' :'+user+', here are the channel indices you requested:\nPRIVMSG '+channel+' :':
            stringer = 'PRIVMSG '+channel+' :The options you specified were garbage. Try #chaoscore or #chaoscore-learning?'
    else:
        stringer=  stringer + "You didn't request any options. Try using 'Index show.'"
    return stringer

def Mime(channel,user,listy,*args):
    return 'PRIVMSG '+channel+' :'+l2s(listy)

def PM(channel,User,listy,*args):
    if len(listy) >1:
        return 'PRIVMSG '+listy.pop(0)+' :'+l2s(listy)
    else:
        return 'PRIVMSG '+channel+' :Sorry, '+User+', but you specified too few arguments for me to PM.'

def Broadcast(channel,User,listy,s,stg,*args):
    if len(listy) > 0:
        if not listy[0] in MasterBotter.Storage.Channels:
            return 'PRIVMSG '+channel+' :It would help if you specified a valid index. Try using the Index command first.'
        stringer = ''
        for item in listy:
            if item[0] == ':':
                message = l2s(listy[listy.index(item):])
                listy2 = listy[:listy.index(item)]
                break
        else:
            return 'PRIVMSG '+channel+' :Please specify a message to send by prefixing the character ":" to the first word of the message.'
        for item in listy2:
            try: MasterBotter.Storage.Channels[item]
            except KeyError:
                stringer = stringer + 'PRIVMSG '+channel+' :The index '+item+' does not exist!\n'
                continue
            for thing in MasterBotter.Storage.Channels[item]:
                if channel != thing:
                    stringer = stringer + '\nPRIVMSG ' +thing+ ' :Broadcast from '+User+': ' + message
            print stringer
        return stringer
    else:
        return 'PRIVMSG '+channel+' :OPTIONS! I need Options!!'

def Bot(channel,User,listy,*args):
    if len(listy)>0:
        return 'PRIVMSG '+channel+' :\x01ACTION '+l2s(listy)+' \x01'
    else:
        return 'PRIVMSG '+channel+" :I can't act without directions!"

def Join(channel,User,listy,*args):
    stringer = 'JOIN '+channel+'\n'
    for item in listy:
        stringer = stringer +'JOIN '+item+'\n'
    return stringer

def Leave(channel,Users,listy,*args):
    if len(listy) > 0:
        stringer = ''
        for item in listy:
            stringer = stringer + 'PART '+item+'\n'
        return stringer
    else:
        return 'PART '+channel

def Bookmark(channel,Users,listy,*args):
    check = False
    stringer = ''
    if not channel in MasterBotter.Storage.Channels['Master']:
        MasterBotter.Storage.Channels['Master'].append(channel)
    for item in listy:
        try: MasterBotter.Storage.Channels[item]
        except KeyError:
            stringer = stringer + 'PRIVMSG '+channel+' :Index '+item+' does not exist!\n'
            continue
        if channel in MasterBotter.Storage.Channels[item]:
            check = True
        if not check:
            MasterBotter.Storage.Channels[item].append(channel)
            stringer =  stringer + 'PRIVMSG '+channel+' :Bookmarked in index '+item+'!\n'
        else:
            stringer = stringer + 'PRIVMSG '+channel+" :I've already bookmarked this channel in this index!\n"
    if stringer == '': return 'PRIVMSG '+channel+" :What index should I bookmark this under?"
    else: return stringer

def DelChannelIndex(channel,Users,listy,*args):
    if len(listy)>0:
        stringer = ''
        for item in listy:
            try: MasterBotter.Storage.Channels.pop(item)
            except KeyError:
                stringer = stringer + 'PRIVMSG '+channel+' :The index '+str(item)+' does not exist!\n'
                continue
            stringer = stringer + 'PRIVMSG '+channel+' :Deleted index '+str(item)+'!\n'
        return stringer
    return 'PRIVMSG '+channel+' :I need indices to check if you want me to do anything'

def CreateChannelIndex(channel,Users,listy,*args):
    if len(listy) > 0:
        stringer = ''
        for item in listy:
            MasterBotter.Storage.Channels[item]= []
            stringer = stringer + 'PRIVMSG '+channel+' :Created Channel Index '+item+'\n'
        return stringer
    else:
        return 'PRIVMSG '+channel+' :I need a channel index to create!'

def UnBookmark(channel,User,listy,*args):
    stringer = ''
    if len(listy) >0:
        for item in listy:
            try: MasterBotter.Storage.Channels[item]
            except KeyError:
                stringer = stringer + 'PRIVMSG '+channel+' :Index '+item+' does not exist!\n'
                continue
            try: MasterBotter.Storage.Channels[item].pop(MasterBotter.Storage.Channels[item].index(channel))
            except ValueError:
                stringer = stringer +'PRIVMSG '+channel+' :Index '+item+' does not contain this channel.\n'
                continue
            stringer = stringer + 'PRIVMSG '+channel+' :This channel has been removed from Index '+item+'\n'
    else: stringer = 'PRIVMSG '+channel+' :I need more arguments to successfully execute this command'
    return stringer

Memo = Mem()

def InviteMe(channel,User,listy,*args):
    stringer = ''
    if len(listy)==0:
        stringer = 'PRIVMSG '+channel+' :Where would you like to be invited, '+User+'?'
    else:
        if listy[0] == 'all' or 'a' in listy:
            stringer = 'PRIVMSG '+channel+' :Inviting '+User+' to channels in the all index!\n'
            for item in MasterBotter.Storage.Channels['a']:
                stringer = stringer + 'INVITE '+User+' :'+item+'\n'
        elif 'Master' in listy:
            stringer = 'PRIVMSG '+channel+' :Inviting '+User+' to channels in the Master index!\n'
            for item in MasterBotter.Storage.Channels['a']:
                stringer = stringer + 'INVITE '+User+' :'+item+'\n'
        else:
            stringer = 'PRIVMSG '+channel+' :Method needs implementation!'
#            for item in listy:
                
#            stringer = 'PRIVMSG '+channel+' :Inviting '+User+' to '+l2s(listy)+'\n'
 #           for item in listy:
  #              stringer = stringer + 'INVITE '+User+' :'+item+'\n'
    return stringer

def PermOpMe(channel,user,*args):
    return 'PRIVMSG CHANSERV :flags '+channel+' '+user+' +*'

def OpMe(channel,user,listy,*args):
    if len(listy) == 0:
        return 'MODE '+channel+' +o '+user
    else:
        return 'MODE '+channel+' +o '+listy[0]

def DeOp(channel,user,listy,*args):
    if len(listy) > 0:
        return 'MODE '+channel+' -o '+str(listy[0])
    else:
        return 'PRIVMSG '+channel+' :I need a user to take ops from!'

def AddUser(channel,user,listy,*args):
    if len(listy) >= 2:
        MasterBotter.Storage.Users[listy[0]] = int(listy[1])
        return 'PRIVMSG '+channel+' :Added user '+listy[0]+' to the permissions dictionary at level '+str(listy[1])
    else:
        return 'PRIVMSG '+channel+' :I need more options to add a user.'

def DelUser(channel,user,listy,*args):
    try: permission = MasterBotter.Storage.Users.pop(listy[0])
    except KeyError:
        return 'PRIVMSG '+channel+" :I don't know that user!"
    return "PRIVMSG "+channel+" :Removed user "+listy[0]+' at permission level '+str(permission)

def InviteUser(channel,user,listy,*args):
    if len(listy) >0:
        User = listy.pop(0)
        if listy[0] == 'all':
            stringer = 'PRIVMSG '+channel+' :Inviting '+User+' everywhere!\n'
            for item in MasterBotter.Storage.Channels:
                stringer = stringer + 'INVITE '+User+' :'+MasterBotter.Storage.Channels[item]+'\n' 
        else:
            stringer = 'PRIVMSG '+channel+' :Inviting '+User+' to: '+l2s(listy)+'\n'
            for item in listy:
                if item[0] == '#':
                    stringer = stringer + 'INVITE '+User+' '+item+'\n'
    else:
        stringer = 'PRIVMSG '+channel+' :Who would you like me to invite?'
    return stringer

def Request(channel,user,listy,*args):
    os.chdir('./UserData/')
    try: file1 = open('suggestions.txt','r+')
    except IOError:
        file1 = open('suggestions.txt','w+')
    file1.readlines()
    file1.write(user + ' '+l2s(listy))
    file1.close()
    os.chdir('..')
    return 'PRIVMSG '+channel+' :Added your request for: '+l2s (listy)

def xkcd(channel,*args):
    return 'PRIVMSG '+channel+' :Here is a random xkcd comic! http://xkcd.com/'+str(random.randint(1,1125))+'/'

def Help(channel,User,listy,s,stg,*args):
    channel = User
    if len(listy) == 0:
        newlist = []
        try: permission = MasterBotter.Storage.Users[User]
        except KeyError:
            permission = 0
        for item in Memo.cmds.keys():
            if permission >= Memo.Permissions[item]:
                newlist.append(item)
        return 'PRIVMSG '+channel+' :For a user of your permissions, I know the following commands: '+l2s(newlist)+'\nPRIVMSG '+channel+' :To use my commands properly, first target me with !Target, then use the command. IE, !* Help\nPRIVMSG '+channel+' :I respond to the following names: '+l2s(map(lambda x: '!'+x+', ',stg.CI['RespondTo']))[:-2]+'.\nPRIVMSG '+channel+' :I also take requests from anyone (not just my owners) using "!Request {suggestion}" or "!request {suggestion}"'

def CodeLink(channel,*args):
    return 'PRIVMSG '+channel+' :Here is a link to my source code: '+zipIt.zipit()+'\n PRIVMSG '+channel+' :Be SURE to open and make the necessary changes in ./NewData/Data.txt!'

def Reload(channel,User,listy,s,*args):
    reload(zipIt)
    return (1,1)

def Reboot(channel,User,listy,s,*args):
    s.send('PRIVMSG '+channel+' :Going down for reboot!\n')
    return (1,0)

def Reconnect(channel,User,listy,s,*args):
    s.send('PRIVMSG '+channel+' :Reconnecting, be right back!\n')
    return (1,-1)

def Quit(channel,User,listy,s,*args):
    s.send('PRIVMSG '+channel+' :Hope to see you again soon!\n')
    return (0,-1)

def SaveData(channel,*args):
    MasterBotter.Store()
    return 'PRIVMSG ' +channel+' :Stored all of the data I can!'

def UserList(channel,*args):
    string = 'PRIVMSG '+channel+' :I know the following users and their permission level:\n'
    for key in MasterBotter.Storage.Users:
        string = string + 'PRIVMSG '+channel+' :User: '+key+' at permission level: '+str(MasterBotter.Storage.Users[key])+'\n'
    return string

def UpdateCode(channel,*args):
    os.system('touch ../MasterBot/')
    return 'PRIVMSG '+channel+' :New code requests will have a new download link!'

def initcmds(Memory = Memo):
   # Memory.cmds['Win'],Memory.Permissions['Win'] = Win, 0
   # Memory.cmds['Kick'],Memory.Permissions['Kick'] = Kick,70
  #  Memory.cmds['Index'],Memory.Permissions['Index'] = Index,0
  #  Memory.cmds['Mime'],Memory.Permissions['Mime'] = Mime,10
  #  Memory.cmds['PM'],Memory.Permissions['PM'] = PM,10
 #   Memory.cmds['Broadcast'],Memory.Permissions['Broadcast'] = Broadcast,30
#    Memory.cmds['Bot'],Memory.Permissions['Bot'] = Bot,10
#   Memory.cmds['Leave'],Memory.Permissions['Leave'] = Leave,90
#    Memory.cmds['Join'],Memory.Permissions['Join'] = Join,90
#    Memory.cmds['Bookmark'],Memory.Permissions['Bookmark'] = Bookmark,90
 #   Memory.cmds['UnBookmark'],Memory.Permissions['UnBookmark'] = UnBookmark,90
    Memory.cmds['Help'],Memory.Permissions['Help'] = Help,0
    Memory.cmds['InviteMe'] ,Memory.Permissions['InviteMe'] = InviteMe,10
    Memory.cmds['InviteUser'] ,Memory.Permissions['InviteUser']= InviteUser,30
#    Memory.cmds['CreateChannelIndex'] ,Memory.Permissions['CreateChannelIndex']= CreateChannelIndex,90
    Memory.cmds['xkcd'] ,Memory.Permissions['xkcd']= xkcd,0
  #  Memory.cmds['OpMe'] ,Memory.Permissions['OpMe']= OpMe,70
    Memory.cmds['PermOpMe'],Memory.Permissions['PermOpMe'] = PermOpMe,90
    Memory.cmds['CodeLink'],Memory.Permissions['CodeLink'] = CodeLink,0
 #   Memory.cmds['AddUser'],Memory.Permissions['AddUser'] = AddUser,70
   # Memory.cmds['!Reload'],Memory.Permissions['!Reload'] = Reload,90
  #  Memory.cmds['!Reboot'],Memory.Permissions['!Reboot'] = Reboot,90
 #   Memory.cmds['!Reconnect'],Memory.Permissions['!Reconnect'] = Reconnect,90
#    Memory.cmds['!Quit'],Memory.Permissions['!Quit'] = Quit,90
    Memory.cmds['SaveData'],Memory.Permissions['SaveData'] = SaveData,90
    Memory.cmds['UserList'],Memory.Permissions['UserList'] = UserList,30
    Memory.cmds['Request'],Memory.Permissions['Request'] = Request,0
    Memory.cmds['DelUser'],Memory.Permissions['DelUser'] = DelUser,90
    Memory.cmds['DeOp'],Memory.Permissions['DeOp'] = DeOp,90
    Memory.cmds['UpdateCode'],Memory.Permissions['UpdateCode'] = UpdateCode,90

initcmds()

def commands(Command,channel,User,extras,s,Stg,Memory = Memo):
    if Command == '':
        return 'PRIVMSG '+channel+' :Greetings, Commodore!'
    if Command[0].islower():
        Command = Command[0].upper() + Command[1:]
    if len(extras) > 0:
        if Command != 'OpMe':
            extras,channel = chcheck(extras,channel)
        else:
            extras,User2 = chcheck(extras,channel)
            if User2[0] == '#':
                channel = User2
            else:
                extras = [User2]
    try: permission = MasterBotter.Storage.Users[User]
    except KeyError:
        permission = 0
    print Command,channel,User,extras
    try: Memory.cmds[Command]
    except KeyError:
        return 'PRIVMSG '+channel+' :I wonder if these silly humans will ever learn...\nPRIVMSG '+channel+" :Until you program it in, IT WON'T WORK.\n"
    print permission,int(Memory.Permissions[Command])
    if permission >= int(Memory.Permissions[Command]):
        return Memory.cmds[Command](channel,User,extras,s,Stg,Memory)
    else:
        return 'PRIVMSG '+channel+ ' :Sorry, you are not authorized to perform this command!'

