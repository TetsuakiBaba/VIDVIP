import os
import glob
import sys
args = sys.argv


def renameWithParentDirName(_files):
    for f in files:
        name_parent_directory = os.path.basename(os.path.dirname(os.path.abspath(f)))   
        filename =  os.path.basename(f)
        ftitle, text = os.path.splitext(filename)
        print 'Rename:', filename , 'to', name_parent_directory+'_'+filename
        os.rename(f, args[1]+'/'+name_parent_directory+'_'+filename)
    return

files = glob.glob(args[1]+'/*.txt')
print args[1]+'/*.txt'
renameWithParentDirName(files)

files = glob.glob(args[1]+'/*.jpg')
print args[1]+'/*.jpg'
renameWithParentDirName(files)