import sys, os

MAIN_DIR = os.path.split(os.path.abspath(sys.argv[0]))[0]
os.chdir(MAIN_DIR)
try:
    libdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lib')
    sys.path.insert(0, libdir)
except:
    sys.exit()

import game
game.run()