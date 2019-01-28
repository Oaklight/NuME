import os
from tinytag import TinyTag
_DEBUG = True

pathToMusic = input("Pls specify the full path to music folder:")
musicList = os.listdir(pathToMusic)
exceptionList = []
reserved = "<>:\"\\/|?*"

for each in musicList:
    fileName, fileExtension = os.path.splitext(each)
    eachPath = os.path.join(pathToMusic, each)
    try:
        tag = TinyTag.get(eachPath)
        if (tag.title is None) or (tag.artist is None):
            exceptionList.append(each)
        else:
            newName = '{} - {}'.format(tag.title, tag.artist)
            newName = newName.replace('/', '.')
            if newName != fileName:
                newPath = newName + fileExtension
                if not _DEBUG:
                    os.rename(each, newPath, pathToMusic, pathToMusic)
                else:
                    print(newPath)
    except:
        exceptionList.append(each)

print('''
Now let\'s process failure cases
''')

for each in exceptionList:
    fileName, fileExtension = os.path.splitext(each)
    eachPath = os.path.join(pathToMusic, each)
    try:
        temp = fileName.replace('_', ' - ')
        fileName = temp if temp != fileName else fileName
        pre, post = fileName.split(' - ')
        propose = post + ' - ' + pre
        switch = input('''
        Choose  1. {}
                2. {}'''.format(fileName, propose))
        if int(switch) == 2:
            newPath = propose + fileExtension
            if not _DEBUG:
                os.rename(each, newPath, pathToMusic, pathToMusic)
            else:
                print(newPath)
    except:
        pass