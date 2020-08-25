import os,csv
import time
from os.path import isfile, isdir, join
from os import listdir

address = os.path.dirname(os.path.abspath(__file__)) + "\\"

print("__file__: "+__file__)

print("os.getcwd(): " + os.getcwd())

print("os.path.dirname(__file__): " + os.path.dirname(__file__))

print("os.path.abspath(__file__): " + os.path.abspath(__file__))

print("os.path.dirname(os.path.abspath(__file__): " + os.path.dirname(os.path.abspath(__file__)))

print("os.path.abspath("".."")" + os.path.abspath("..") )

print(os.path.abspath("..") + "\\Data\\Mobile\\M_Data\\" )

files = listdir(os.path.abspath("..") + "\\Data\\Mobile\\M_Data\\" )

print(files)