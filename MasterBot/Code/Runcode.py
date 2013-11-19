import socket
import commandant
import MasterBotter
import BotTalking
import zipIt

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
                MasterBotter.Storage.Users[line[1:-3]] = line[-2:]

def init(S,Stg):
    S.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    S.connect((Stg.CI['HOST'],int(Stg.CI['PORT'])))
    S.send('USER '+Stg.CI['IDENT']+' '+Stg.CI['HOST']+' '+Stg.CI['OWNER']+' :' + Stg.CI['REALNAME']+ ' Script\n')
    S.send('NICK '+Stg.CI['NICK']+'\n')
    identified = 0
    while not identified:
        line = S.recv(1024)
        if line != '':
            print line
        if 'End of /MOTD' in line:
            S.send('NS identify '+Stg.CI['PASS']+'\n')
        if 'You are now identified' in line:
            identified = 1
    for item in MasterBotter.Storage.Channels['Master']:
        S.send('ChanServ :invite '+item+' \n')
        line = ''
        while not 'invited' in line and not 'Insufficient' in line and not 'authorized' in line and not 'already' in line and not 'registered' in line:
            line = line + S.recv(1024)
            if line != '':
                print line
        S.send('JOIN '+item+'\n')
    return

def running(S,Stg):
    line = S.recv(1024)
    listitems = []
 #   for key in BotTalking.DataStuff.oC:
  #      if BotTalking.DataStuff.oC[key].recv(1024) != '':
   #         listitems.append(BotTalking.DataStuff.oC[key].recv(1024))
   # if len(listitems) > 0:
    #    print listitems
    if line != '':
        line2 =line.split()
        print line2
        if line2[0]=='PING':
            S.send('PONG '+line2[1]+'\n')
            return 1,1
        if 'Gio77' in line and 'JOIN' in line:
            S.send('MODE '+line2[-1]+' +v Gio77\n')
#        if '[CCB]' in line and ('JOIN' in line or 'PART' in line) and '#chaoscorebots' in line:
 #           print "Maintenance!"
  #          MasterBotter.Maintenance(S,Stg)
        if ('QUIT' in line and Stg.CI['NICK'] in line) or 'timed' in line:
            return 1,-1
        bang = line2[0].find('!')
        Commander = line2[0][1:bang]
        for x in range(3,len(line2)):
            named = line2[x][2:]
            if named == 'Request' or named == 'request' or named == 'Help' or named == 'help':
                Commander = named
                named = '*'
            if ':!' in line2[x] and named in Stg.CI['RespondTo'] :
                if line2[2][0] == '#':
                    channel = line2[2]
                else:
                    channel = Commander
                newl = line2[x+1:]
                try: comander = newl.pop(0)
                except IndexError:
                    comander = ''
                ret = commandant.commands(comander,channel,Commander,newl,S,Stg)
                if ret == (0,1):
                    reload(commandant)
                    reload(zipIt)
                    S.send('PRIVMSG '+channel+' :Reloaded ALL commands!\n')
                    return (1,1)
                if ret in [(1,0),(1,-1),(0,-1)]:
                    MasterBotter.Store()
                    return ret
                else:
                    print "Sending this message to server: ", ret
                    S.send(ret+'\n')
#                try: file1 = open('suggestions.txt','r+')
 #               except IOError:
  #                  file1 = open('suggestions.txt','w')
   #             file1.readlines()
   #             file1.write(line)
   #             file1.close()
   #         if ':!' in line2[x] and Commander in Stg.OU:
   #             print 'dat'
   #             named = line2[x][2:]
   #             channel = line2[2]
   #             newl = line2[x+1:]
  #              try: comander = newl.pop(0)
  #              except IndexError:
  #                  comander = ''
  #              print Commander, comander,channel,newl
  #              if Stg.CI['NICK'] == named or named == '*' or named == Stg.CI['NICK'][:5] or named == Stg.CI['NICK'][5:]:
  #                  print name, comander,channel,newl, named, Stg.CI['NICK']
  #                  if comander == '!Reload':
  #                      MasterBotter.Store()
  #                      reload(MasterBotter)
  #                      reload(commandant)
  #                      S.send('PRIVMSG '+channel+' :Reloaded ALL commands!\n')
  #                      break
  #                  elif comander == '!Reboot':
  #                      S.send('PRIVMSG '+channel+' :Going down for reboot!\n')
  #                      MasterBotter.Store()
  #                      reload(MasterBotter)
  #                      reload(commandant)
  #                      print "Rebooting"
  #                      return 1,0
  #                  elif comander == '!Reconnect':
  #                      S.send('PRIVMSG '+channel+' :Reconnecting, be right back!\n')
  #                      MasterBotter.Store()
  #                      reload(MasterBotter)
  #                      reload(commandant)
  #                      return 1,-1
  #                  elif comander == '!Quit':
  #                      S.send('PRIVMSG '+channel+' :Bye!\n')
  #                      MasterBotter.Store()
  #                      reload(MasterBotter)
  #                      return 0,-1
    return 1,1
