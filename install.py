import pkg_resources
import os
from threading import Thread
import sys

# Fixes the dependencies -- Not a lot of effort put into this

needed = ['pynput', 'matplotlib', 'pyautogui', 'numpy']
package_list = [dist.project_name for dist in pkg_resources.working_set]

def is_package_installed(package_name):
    global package_list
    return package_name in package_list

def check_packages():
    for pkg in needed:
        if not is_package_installed(pkg):
            try:
                os.system(f'pip install {pkg}')
            except:
                exit(f"Package installation error {pkg}")
        
def delete_self():
    __scriptpath__ = os.path.abspath(__file__)
    os.remove(__scriptpath__)
    if sys.platform == 'linux':
        os.sync()
    elif sys.platform == 'darwin':
        os.sync()
    

if __name__ == '__main__':
    checker = Thread(target=check_packages)
    banished = Thread(target=delete_self)
    
    checker.start()
    checker.join()
    banished.start()
    banished.join()
    
