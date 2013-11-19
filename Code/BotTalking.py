import socket
import commands


def myIP():
    ips = commands.getoutput("/sbin/ifconfig | grep -i \"inet\" | grep -iv \"inet6\" | " +
                             "awk {'print $2'} | sed -ne 's/addr\:/ /p'")
    listy = []
    st = ''
    for x in range(len(ips)):
        if ips[x] != '\n':
            st = st + ips[x]
        else:
            listy.append(st.strip())
            st = ''
    listy.append(st.strip())
    for item in listy:
        dot = item.find('.')
        if not item[:dot] in ['10','127','192']:
            return item
    return listy

class ConnectionData():
    def __init__(self):
        self.Bots = {}
        self.oC = {}
        self.IP = '54.243.45.112'
        print "My IP is: ", self.IP

DataStuff = ConnectionData()

def StartConnection(address,Memory =DataStuff):
    Memory.oC[address[1]] = socket.socket()
    Memory.oC[address[1]].connect(address)
    return Memory.oC[address[1]]

def StartServer(port,Memory = DataStuff):
    if not port in Memory.oC:
        Memory.oC[port] = socket.socket()
        Memory.oC[port].bind(('localhost',port))
    return Memory.oC[port]

def connecter(S,stg,otherbot,Memory=DataStuff):
    for port in range(42042,44042):
        if not port in Memory.oC:
            break
    sock = StartServer(port)
    S.send('PRIVMSG '+otherbot+' :Please Connect to: (' + str(Memory.IP)+', '+ str(port)+')\n')
    print "sent"
    line = ''
    while line == '':
        thing = sock.listen(1024)
        if thing != None:
            print thing

def makeConnect(bot,port,Memory = DataStuff):
    Memory.Bots[bot] = port

def receiver(S,stg,otherbot,Memory=DataStuff):
    line = ''
    print "Rec"
    while not 'Please Connect to:' in line:
        line = line + S.recv(1024)
    host = line[line.find('(')+1:line.find(',')]
    port = line[line.find(',')+1:line.find(')')]
    print host,port
    StartConnection((host,int(port)))
    makeConnect(otherbot,int(port))
    print Memory.Bots[otherbot]
    return (host,int(port))

def sendit(data,bot,Memory=DataStuff):
    Memory.oC[Memory.Bots[bot]].send(data)

def ConnectedTo(Memory = DataStuff):
    stringed = ''
    for item in Memory.oC:
        stringed = stringed + item + ' '
    return stringed
