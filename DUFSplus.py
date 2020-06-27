#Modules
import configparser, os, subprocess, time, easygui

#Init
config = configparser.ConfigParser()
config.read("config.ini")


#Run steam as new user specified in .ini
if config['SETTINGS']['BPM']:
    process = subprocess.run('runas  /user:' + config['SETTINGS']['NewUser'] + ' /savecred "' + config['PATHS']['SteamPath'] + ' -bigpicture"')
else:
    process = subprocess.run('runas  /user:' + config['SETTINGS']['NewUser'] + ' /savecred "' + config['PATHS']['SteamPath'] + '"') 
if not process.returncode == 0:
    easygui.msgbox("Something went wrong starting steam as user: " + config['SETTINGS']['NewUser'] + ". Check you have entered the correct details in DUFSConfig.ini", 'Error: Cannot start steam.exe as ' + config['SETTINGS']['newuser'])
    quit()

#Raise steam.exe priority if highpriority is set to True in DUFSConfig.ini
if config.getboolean('SETTINGS', 'highpriority'):
    process = subprocess.run('wmic process where name="steam.exe" call setpriority "128"')
    if not process.returncode == 0:
        easygui.msgbox("Something went wrong raising the priority of steam. Should the issue persist, raise and issue on github", 'Error: Cannot raise priority of steam.exe')
        quit()

#Wait for steam home streaming users to reconnect
time.sleep(int(config['SETTINGS']['Client-GameWaitTime']))

#Start game
os.rename(config['PATHS']['GamePath'], config['PATHS']['GamePath'] + r'.bak')
os.rename(config['PATHS']['GamePath'].replace('.exe', '-Temp.exe'),  config['PATHS']['GamePath'])

if config['PATHS']['UseGameID']:
    process = subprocess.run(config['PATHS']['SteamPath'] + ' -applaunch ' + config['PATHS']['GameID'])
else:
    process = subprocess.run('runas /savecred /user:' + config['SETTINGS']['NewUser'] + ' /savecred "' + config['PATHS']['GamePath'] + '"')
    print('Started game: ' + os.path.basename(config['PATHS']['GamePath']))

processName = os.path.basename(config['PATHS']['MonitorEXE'])

#Continuously check if the process still exists
time.sleep(20)

while True:
    print('Process check loop')
    time.sleep(int(config['SETTINGS']['processcheckfrequency']))
    print('Waited ' + config['SETTINGS']['processcheckfrequency'] + " seconds")
    process = subprocess.check_output('TASKLIST /FO "LIST" /FI "IMAGENAME eq ' + processName)
    if not processName in str(process):
        print('Process no longer exists. Killing steam.exe')
        process = subprocess.run('taskkill /IM "steam.exe" /F', capture_output=True)
        if not process.returncode == 0:
            easygui.msgbox('Something went wrong with killing the steam process. Check DUFSLog.txt for more. Should the issue persist, raise an issue on github', 'Error: Cannot kill steam.exe')
            quit()
        os.rename(config['PATHS']['gamepath'], config['PATHS']['gamepath'].replace('.exe', '-Temp.exe'))
        os.rename(config['PATHS']['gamepath'] + r'.bak', config['PATHS']['gamepath'])
        print("Running steam.exe as normal user")
        subprocess.run('runsteam.bat')
        if config.getboolean('SETTINGS', 'highpriority'):
            process = subprocess.run('wmic process where name="steam.exe" call setpriority "128"')
            if not process.returncode == 0:
                easygui.msgbox("Something went wrong raising the priority of steam. Check DUFSLog.txt for more. Should the issue persist, raise and issue on github", 'Error: Cannot raise priority of steam.exe')
                quit()
        print("Job here is done, quitting now..")
        break