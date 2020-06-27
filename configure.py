#Modules
import easygui, os, configparser, getpass, PyInstaller.__main__

#Init
if not os.path.exists('DUFSplus'):
    os.makedirs('DUFSplus')

config = configparser.ConfigParser()
log = open('DUFSplus/Log.txt', 'w')

#Gather information for config file
gameID = None
pathSteam = easygui.fileopenbox("Select 'steam.exe'", "Point DUFS to Steam Client", "C:/Program Files (x86)/Steam/*.exe")
installLocation = easygui.diropenbox('Select game install directory', 'Point DUFS to game install folder', 'C:/Program Files (x86)/Steam/steamapps/common')
steamOrPath = easygui.ynbox('Tell DUFS to launch the game using it\'s steam game ID?', 'Use GameID')
if steamOrPath:
    gameID = easygui.enterbox('Enter the steam game ID: (use steamdb.info to find this if you do not know it already)', "Enter Steam Game ID")
pathGame = easygui.fileopenbox("Select Game exe", "Point DUFS to Game Executable", installLocation)
monitor = easygui.fileopenbox("Select executable to monitor", "Point DUFS towards the executable DUFS will continually check is running", installLocation)
usr = easygui.enterbox('Enter new user game will launch as. Needs to be in the pattern DOMAIN\\USER', "Enter new User details")
bpm = easygui.ynbox('Use Steam Big Picture Mode?', "Use BPM?")

#Write information to config file
config['PATHS'] = { 'SteamPath': pathSteam,
                    'InstallLocation': installLocation,
                    'UseGameID': steamOrPath,
                    'GameID': gameID,
                    'GamePath': pathGame,
                    'MonitorEXE': monitor
}
config['SETTINGS'] = { 'NewUser': usr,
                        'BPM': bpm,
                        'Client-GameWaitTime': 20,
                        'ProcessCheckFrequency': 10,
                        'HighPriority': False
}
with open('config.ini', 'w') as ini:
    config.write(ini)

#Create launch script
pyscript = """import os
config = configparser.ConfigParser()
config.read('DUFSplus/config.ini')
os.system('Taskkill /IM "steam.exe" /F')
os.system('runas /user:' + config['SETTINGS']['NewUser'] + ' /savecred "DUFSplus/DUFSplus.exe"')"""
with open('launch.py', 'w') as launch:
    launch.write(pyscript)

PyInstaller.__main__.run(['-F', '-n' + str(pathGame.rsplit('\\', 1)), 'launch.py'])

#Create steam restart script
with open('steamRestart.bat', 'w') as steam:
    steam.write('runas /user:' + getpass.getuser() + '/savecred "' + pathSteam + '"')