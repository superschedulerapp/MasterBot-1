import socket
import commandant
import MasterBotter
import BotTalking
import zipIt
import cmds
import time

class Datas():
    def __init__(self, Filer):
        self.CI = {}
        self.OU = {}
        self.CN = {}
        self.chans = {}
        self.OB = {}
        self.users = {}
        self.US = set()
        self.US.add('@')
        self.US.add(':')
        self.US.add('+')
        ChanNum = 0
        for line in Filer:
            if line[-1] == '\n':
                line = line[:-1]
            if line == '':
                continue
            if line[0] == '%':
                comma =line.find(',')
                cmd = line[1:comma]
                if cmd == 'RespondTo':
                    cmd2 = line[(comma+1):].split()
                else:
                    cmd2 = line[(comma+1):]
                self.CI[cmd] = cmd2
            elif line[0] == '#' and not line[1] == '#':
                self.CN[ChanNum] = line
                ChanNum += 1
            elif line[0] == '@':
                self.OU[line[1:-3]] = line[-2:]
                MasterBotter.Storage.Users[line[1:-3]] = int(line[-2:])

def init(S,Stg):
    S.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    S.settimeout(300.0)
    S.connect((Stg.CI['HOST'],int(Stg.CI['PORT'])))
    S.send('USER '+Stg.CI['IDENT']+' '+Stg.CI['HOST']+' '+Stg.CI['OWNER']+' :' + Stg.CI['REALNAME']+ ' Script\n')
    S.send('NICK '+Stg.CI['NICK']+'\n')
    identified = 0
    while not identified:
        line = ''
        while not '\n' in line:
            line = line + S.recv(1)
        print line
        if 'End of /MOTD' in line or 'registered' in line:
            S.send('NS identify '+Stg.CI['PASS']+'\n')
        if 'You are now identified' in line:
            identified = 1
    try: MasterBotter.Storage.Channels['Master']
    except KeyError:
        return
    for item in MasterBotter.Storage.Channels['Master']:
        S.send('ChanServ :invite '+item+' \n')
        line = ''
        while not 'invited' in line and not 'Insufficient' in line and not 'authorized' in line and not 'already' in line and not 'registered' in line:
            line = line + S.recv(1)
        S.send('JOIN '+item+'\n')
    return

def running(S,Stg):
    line = ''
    while not '\n' in line:
        try:line = line + S.recv(1)
        except: return 1,-1
    line2 =line.split()
    print line2
    if line2 == []:
        return 1,2
    if line2[0]=='PING':
        S.send('PONG '+line2[1]+'\n')
        return 1,2
    if ('QUIT' in line and Stg.CI['NICK'] in line) or 'timed' in line:
        return 1,-1
    for x in range(3,len(line2)):
        if ':!' in line2[x]:
            ret = cmds.commands(line2,S,Stg)
            keylist = ret.keys()
            keylist.sort()
            for key in keylist:
                if key == 0:
                    for item in ret[key]:
                        S.send(item + '\n')
                if key == 2:
                    pass
                if key == 9:
                    return ret[key]
            break
    return 1,2
