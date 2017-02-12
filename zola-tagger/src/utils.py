'''
Created on Feb 3, 2017

@author: Stefan

Some handy utility functions.

'''

import os

def getParentFolderAndFileName(filename):
    '''Given a string containing a file path (absolute or relative),
    retrieve a string containing only the parent folder name and file name,
    separated by the os.path.sep separator.'''
    return os.path.join(os.path.basename(os.path.dirname(filename)), os.path.basename(filename))