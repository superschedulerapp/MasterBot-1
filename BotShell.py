from Code import importData
importData.initData()
import socket
import time
from Code import Runcode, BotTalking, MasterBotter,cmds
import os

run = 2
Connected = 1
importData.initData()
while Connected:
    Socker = socket.socket()
    Storg = Runcode.Datas(open('./UserData/Data.txt','r'))
    Runcode.init(Socker,Storg)
    Connected,run = 1,1;print "Connected!"
    while run >=0:
        Storg = Runcode.Datas(open('./UserData/Data.txt','r'))
        run = 1; print "Booted"
        while run > 0:
            run = 2; print "Loaded"
            while run > 1:
                Connected,run = Runcode.running(Socker,Storg)
            MasterBotter.Store()
            if Connected > 0:
                cmds.Memo = cmds.Mem()
                reload(cmds)
                cmds.Memo = cmds.Mem()
        if Connected > 0:
            reload(Runcode)
    if Connected > 0:
        reload(MasterBotter)
        reload(BotTalking)
    Socker.close()
