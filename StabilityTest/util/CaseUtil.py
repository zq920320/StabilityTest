import os
import os.path
from StabilityTest import app


def getFloder(name):
    rootdir = app.config['FITNESSE_ROOT']
    rootdir = rootdir + "/" + name
    floders = []
    print floders
    for parent, dirnames, filenames in os.walk(rootdir):
        for dirname in dirnames:
            floders.append(dirname)
    return floders
