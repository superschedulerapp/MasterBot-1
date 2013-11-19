from Code import importData
importData.initData()
import socket
import time
from Code import Runcode, BotTalking, MasterBotter,cmds
import os

#This is the main script which runs everything. 
#Its only job is to interpret the return value from Runcode.running()
#and execute what needs to happen based on the two variables, 
#and then execute .running() again (unless connected == 0, which is
#what is returned upon using the !Quit command.)

run = 2
Connected = 1
importData.initData()
while Connected:
    Socker = socket.socket()
    os.system('dir')
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
