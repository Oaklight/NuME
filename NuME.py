import os, sys
from tinytag import TinyTag
_DEBUG = False
reserved = ['<', '>', ':', '\"', '\\', '/', '|', '?', '*']
artist = set()

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
                artist.add(str(tag.artist).title())
                propose = sanityCheck('{} - {}'.format(tag.title, tag.artist))
        except:
                propose = abnormal(filename)
        
        if propose != filename:
            newPath = os.path.join(pathToMusic, propose + fileExtension)
            if not _DEBUG:
                try:
                    os.rename(os.path.join(pathToMusic, each), newPath)
                except:
                    newPath = os.path.join(
                        pathToMusic, 
                        propose.replace(' - ', '2 - ') + fileExtension
                    )
                    os.rename(os.path.join(pathToMusic, each), newPath)
            else:
                print(newPath)

def abnormal(filename):
    try:
        temp = filename.replace('_', ' - ')
        filename = temp if temp != filename else filename
        
        pre, post = filename.split(' - ')
        if pre in artist:
            propose = post + ' - ' + pre
        elif post in artist:
            propose = filename
        else:
            propose = post + ' - ' + pre
            switch = input('''
            Choose the correct one:  
                1. {}
                2. {}
                '''.format(filename, propose)) 
                    #1. post in artist; 2. pre in artist

            if int(switch) == 1:
                propose = filename
                artist.add(post)
            elif int(switch) == 2:
                artist.add(pre)

    except:
        propose = input("Unknown error! Pls check this filename: {}: ".format(filename))
    return propose

def sanityCheck(propose):
    for each in reserved:
        propose = propose.replace(each, '.')
    return propose

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
