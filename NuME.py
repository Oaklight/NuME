import os, sys, traceback
from tinytag import TinyTag
_DEBUG = True

def main():
    pathToMusic = input("Pls specify the full path to music folder:")
    musicList = os.listdir(pathToMusic)

    for each in musicList:
        if each == 'desktop.ini':
            continue

        filename, fileExtension = os.path.splitext(each)
        eachPath = os.path.join(pathToMusic, each)
        try:
            tag = TinyTag.get(eachPath)
            if (tag.title is None) or (tag.artist is None):
                propose = abnormal(filename)            
            else:
                propose = '{} - {}'.format(tag.title, tag.artist.replace('/', '.'))
        except:
                propose = abnormal(filename)
        
        if propose != filename:
            newPath = propose + fileExtension

            if not _DEBUG:
                os.rename(each, newPath, pathToMusic, pathToMusic)
            else:
                print(newPath)

def abnormal(filename):
    try:
        temp = filename.replace('_', ' - ')
        filename = temp if temp != filename else filename
        
        pre, post = filename.split(' - ')
        propose = post + ' - ' + pre

        switch = input('''
        Choose  1. {}
                2. {}
                '''.format(filename, propose))
        
        if int(switch) == 1:
            propose = filename
    except:
        propose = input("Unknown error! Pls check this filename: {}.".format(filename))
    return propose

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
    except Exception:
        traceback.print_exc(file=sys.stdout)
    finally:
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
