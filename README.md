MasterBot
=========

Uncrashable Python IRC bot


When first downloaded, moving into the main folder and running BotShell.py will initialize the user data.


Then, you should open up UserData/Data.txt, and change the information contained therein to match what you would like, as far as username, owner, and IRC server are concerned. 


Known bugs: Ogame highscore functionality does not properly deal with connection hangs. The entire script will go down due to the signal method currently in place, which I am unhappy about. Therefore I've simply disabled the Highscore functionality, which shouldn't be a problem unless you really want ogame data. Also, I need to implement something which ensures that cmds doesn't return a string too long to be sent. Currently, the help text will be truncated because of this. 
