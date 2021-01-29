#import os
#import sys
#dirname, _ = os.path.split(os.path.abspath(__file__))
#sys.path.insert(0, dirname+"/Controller")
#sys.path.insert(0, dirname+"/View")
#sys.path.insert(0, dirname+"/Model")
#print(sys.path)
from View.Main_Windows import Main

Main().start()