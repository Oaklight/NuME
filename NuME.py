import os, sys
from mutagen import File
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3

_DEBUG = False
# _VERBOSE = True
_reserved = ['<', '>', ':', '\"', '\\', '/', '|', '?', '*']
_artists = set()

def main():
    pathToMusic = input("Pls specify the full path to music folder:")
    musicList = os.listdir(pathToMusic)

    for each in musicList:
        if each == 'desktop.ini':
            continue

        filename, fileExtension = os.path.splitext(each)
        eachPath = os.path.join(pathToMusic, each)
        # print(filename)
        try: # file type readable
            tag = getTag(eachPath)
            # print(tag)
            if (not tag) or (not tag['title']) or (not tag['artist']): # new tag or incomplete tag
                # print(11111)
                propose = abnormal(filename, tag) # tag missing
            else: # normal tag
                # print(22222)
                _artists.add(tag['artist'][0])
                propose = sanityCheck('{} - {}'.format(tag['title'][0], tag['artist'][0]))
        except: # file type unreadable
            # print('1231231233')
            propose = abnormal(filename) # format unsupported
        
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
            print(newPath)
            print('filename updated')

def abnormal(filename, tag=None):
    try:
        filename = filename.replace('_', ' - ')
        pre, post = filename.split(' - ')
        
        propose = post + ' - ' + pre
        if post in _artists:
            propose = filename
        else:
            switch = input('''
            Which is the title:
                1. {}
                2. {}
            Given file {}
                '''.format(pre, post, filename)) 
            #1. post is artist; 2. pre is artist

            if int(switch) == 1:
                propose = filename
            elif int(switch) == 2: # swap pre and post
                temp = pre
                pre = post
                post = temp
            _artists.add(post) # post is artist, always
            if not _Debug and tag is not None:
                # print(post, pre)
                updateTag(tag, post, pre)
                # print(tag)
    except:
        propose = input("Unknown error! Pls input correct filename for {}: ".format(filename))
    return propose

def getTag(filePath):
    try:
        tag = EasyID3(filePath)
        # print('tag read')
    except:
        # print('tag missing')
        try:
            tag = EasyID3()
            tag.save(filePath)
        except Exception as e:
            print(e)
            print('failed to get tag, check file at {}'.format(filePath))
        # else:
        #     print('tag created')
    finally:
        return tag

def updateTag(tag, artist_name=None, song_name=None):
    try:
        print(artist_name, song_name)
        if artist_name is not None:
            tag['artist'] = artist_name
        if song_name is not None:
            tag['title'] = song_name
        tag.save()
        print('tag updated')
    except:
        print('update failed')
    return tag

def sanityCheck(propose):
    for each in _reserved:
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
