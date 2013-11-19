import os

def initData():
    if not os.path.isdir('./UserData/'):
        os.path.mkdir('./UserData/')
    if not os.path.isfile('./UserData/Data.txt'):
        os.system('cp ./NewData/*.* ./UserData/\n')
