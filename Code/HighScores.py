import urllib2
import signal

#Code specific to Ogame.org, which will parse and return requested
#high score data to the IRC channel. 
#Known problems: Connection timeouts are not handled properly, resulting
#in the script possibly hanging. The solution implemented with signal
#results in the entire scipt being crashed rather than just this one. 
#As this (ogame highscore) fucntionality is non-essential I recommend
#simply disabling rather than attempting to fix. 

HStypes = {0:'Total',1:'Economy',2:'Research',3:'Military',5:'Military Built'
                    ,6:'Military Destroyed',4:'Military Lost',7:'Honor'}

for key in HStypes.keys():
    HStypes[HStypes[key]] = key

def handler(signum, frame):
    print "Signal Handler Called! signal: ", signum
    raise signal.ItimerError("Did not successfully load the URL")

def kwargit(stringy):
    nuStringy = stringy.split()
    retD = {}
    for item in nuStringy:
        nuItem = item.split("=")
        print nuItem
        retD[nuItem[0]] = nuItem[1]
    return retD

def find(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]

def lowerParse(smallString):
    quoteSpots = find(smallString,'"')
    s = 0
    leng = len(quoteSpots)
    rdict = {}
    lastPos = 7
    while s < leng:
        rdict[smallString[lastPos:quoteSpots[s]-1]] = smallString[quoteSpots[s]+1:quoteSpots[s+1]]
        try: lastPos = quoteSpots[s+1]+2
        except: break
        s +=2
    return rdict

def parse(wholeString):
    nuString = wholeString.split('><')
    retDict = {}
    for item in nuString[:-1]:
        info = lowerParse(item)
        try: retDict[int(info['id'])] = info
        except: 
      #      print "NAW", info
            if info != {} and 'timestamp' in info:retDict['universe'] = info
    return retDict

def allyParse(wholeString):
    nuString = wholeString.split('><')
    retDict = {}
    allianceInfo = lowerParse(nuString[1])
    alliance = allianceInfo['tag']
    retDict[alliance] = allianceInfo
    retDict[alliance]['Players'] = []
    for item in nuString[1:-1]:
        if item[:8] == 'alliance':
            allianceInfo = lowerParse(item)
            alliance = allianceInfo['tag']
            retDict[alliance]  =allianceInfo
            retDict[alliance]['Players'] = []
        else:
            playerInfo = lowerParse(item)
    #        print playerInfo
            try: retDict[alliance]['Players'].append(playerInfo['id'])
            except: pass
    return retDict

def allyScores(rankD, HStype, number,perPlayer = False):
    strings = ['In the category '+ HStypes[HStype]+', the top %i alliances %s are as follows:\n'%(number, 'per player' if perPlayer else '')]
    ranks = rankD[HStype]
    for x in range(number):
        strings.append("Rank {0}: ".format(x+1) + ranks[x][1] + ' with '+str(int(ranks[x][0])) +' points{0}.\n'.format(' per player' if perPlayer else''))
    print strings
    return strings 
    

hiPage =urllib2.urlopen("http://uni120.ogame.org/api/players.xml")
hiPage.readline()
hiScoreDict = {}
scores = hiPage.readline()
Players = parse(scores)
playerNames = {}
for Player in Players:
    try:playerNames[Players[Player]['name']] = Player
    except: pass
hiScores = range(8)
for typed in hiScores:
    done = False
    signal.signal(signal.SIGINT,handler)
    while not done:
        try:
            signal.alarm(10)
            HiScores = urllib2.urlopen("http://uni120.ogame.org/api/highscore.xml?category=1&type=%i" %(typed))
            HiScores.readline()
            thisScores = parse(HiScores.readline())
            for Player in thisScores:
                infos = thisScores[Player]
                try: Players[Player]['hiScores'][typed] = (infos['position'],infos['score'])
                except: 
                    try: Players[Player]['hiScores'] = {typed:(infos['position'],infos['score'])}
                    except: pass
            signal.alarm(0)
            done = True
        except:  pass
allyHiPage =urllib2.urlopen("http://uni120.ogame.org/api/alliances.xml")
Universe = urllib2.urlopen("http://uni120.ogame.org/api/universe.xml")
Universe.readline()
U2 = Universe.readline()
allyHiPage.readline()
Ally2 = allyHiPage.readline()
allianceData = allyParse(Ally2) 
allianceNameTag = {}
for ally in allianceData:
    allianceData[ally]['HighScores'] = {}
    allianceNameTag[allianceData[ally]['name']] = ally
    for x in range(8):
        allianceData[ally]['HighScores'][x] = 0
    for player in allianceData[ally]['Players']:
        try:
            for pos,highscore in enumerate(Players[int(player)]['hiScores']):
                allianceData[ally]['HighScores'][pos]+= int(Players[int(player)]['hiScores'][highscore][1])
        except: pass
rankD = {X:[] for X in range(8)}
perRankD = {X:[] for X in range(8)}
for ally in allianceData:
    players = len(allianceData[ally]['Players'])
    allianceData[ally]['PerPlayer'] = {}
    allianceData[ally]['Rank'] = {X:[0,0] for X in range(8)}
    for x in range(8):
        score = allianceData[ally]['HighScores'][x]
        rankD[x].append((score,ally))
        allianceData[ally]['PerPlayer'][x] = score*1.0/players
        perRankD[x].append((score*1.0/players,ally))
for x in rankD:
    rankD[x].sort()
    rankD[x].reverse()
    perRankD[x].sort()
    perRankD[x].reverse()
for x in rankD:
    for pos,y in enumerate(rankD[x]):
        allianceData[y[1]]['Rank'][x][0] = pos + 1
for x in perRankD:
    for pos,y in enumerate(perRankD[x]):
        allianceData[y[1]]['Rank'][x][1] = pos + 1
print allianceData['LSD'], rankD[0][0], perRankD[0][0]
planetData = parse(U2)
TimeofUpdate = planetData['universe']['timestamp']
#print TimeofUpdate,leadLine,planetData#,U2
f = open("timesave",'r+')
time = f.readline()
f.close()
f = open("timesave","w+")
f.write(TimeofUpdate)
f.close()
for planet in planetData:
    #print planetData[planet]
    try: 
        Players[int(planetData[planet]['player'])]['Planets'].add(planetData[planet]['coords'])
        Players[int(planetData[planet]['player'])]['PlanetsInfo'][planetData[planet]['coords']] = planetData[planet]
    except: 
        try:
            Players[int(planetData[planet]['player'])]['Planets']=set([planetData[planet]['coords']])
            Players[int(planetData[planet]['player'])]['PlanetsInfo'] = {}
            Players[int(planetData[planet]['player'])]['PlanetsInfo'][planetData[planet]['coords']] = planetData[planet]
        except: pass

nf = open("addiLocs","r")
for line in nf:
    newL = line.split()
    Players[playerNames[newL[0]]]['Planets'].add(newL[1])
nf.close()
