import os, sys

from mutagen import File
from mutagen.easyid3 import EasyID3

# _VERBOSE = True
_reserved = ["<", ">", ":", '"', "\\", "/", "|", "?", "*"]
_artists = set()


def main():
    _pathToMusic = input("Pls specify the full path to music folder:")
    musicList = os.listdir(_pathToMusic)

    for each in musicList:
        if each == "desktop.ini":
            continue

        filename, _fileExtension = os.path.splitext(each)

        def _locFile(filename=None):
            return os.path.join(_pathToMusic, filename + _fileExtension)

        currentPath = _locFile(filename)

        # print(filename)
        try:  # file type readable
            tag = getTag(currentPath)
            # print(tag)
            if (
                (not tag) or (not tag["title"]) or (not tag["artist"])
            ):  # new tag or incomplete tag
                propose = abnormal(filename, tag)  # tag missing
            else:  # normal tag
                _artists.add(tag["artist"][0])
                propose = sanityCheck(
                    "{} - {}".format(tag["title"][0], tag["artist"][0])
                )
        except:  # file type unreadable
            propose = abnormal(filename)  # format unsupported

        if propose != filename:
            newPath = _locFile(propose)
            if not __debug__:  # actual test mode
                print("filename proposed: {} --> {}".format(filename, propose))
            else:  # the normal mode
                try:
                    os.rename(currentPath, newPath)
                except:
                    newPath = _locFile(propose.replace(" - ", "2 - "))
                    os.rename(currentPath, newPath)
                # print(newPath)
                print("filename updated: {} --> {}".format(filename, propose))


def abnormal(filename, tag=None):
    try:
        filename = filename.replace("_", " - ")
        pre, post = filename.split(" - ")

        propose = post + " - " + pre
        if post in _artists:
            propose = filename
        else:
            switch = input(
                """
            Which is the title:
                1. {}
                2. {}
            Given file {}
                """.format(
                    pre, post, filename
                )
            )
            # 1. post is artist; 2. pre is artist

            if int(switch) == 1:
                propose = filename
            elif int(switch) == 2:  # swap pre and post
                temp = pre
                pre = post
                post = temp
            _artists.add(post)  # post is artist, always
            if not _Debug and tag is not None:
                # print(post, pre)
                updateTag(tag, post, pre)
                # print(tag)
    except:
        propose = input(
            "Unknown error! Pls input correct filename for {}: ".format(filename)
        )
    return propose


def getTag(filePath):
    try:
        tag = EasyID3(filePath)
        tag.save(filePath)
        # print('tag read')
    except:
        # print('tag missing')
        try:
            tag = EasyID3()
            tag.save(filePath)
        except Exception as e:
            print(e)
            print("failed to get tag, check file at {}".format(filePath))
        # else:
        #     print('tag created')
    finally:
        return tag


def updateTag(tag, artist_name=None, song_name=None):
    try:
        print(artist_name, song_name)
        if artist_name is not None:
            tag["artist"] = artist_name
        if song_name is not None:
            tag["title"] = song_name
        tag.save()
        print("tag updated")
    except:
        print("update failed")
    return tag


def sanityCheck(propose):
    for each in _reserved:
        propose = propose.replace(each, ".")
    return propose


if __name__ == "__main__":
    try:
        if __debug__:
            print("Test OFF, file WILL be changed, unless run with '-O'")
        else:
            print("Test ON, no actual file modification")
        main()
    except (KeyboardInterrupt, SystemExit):
        print("Interrupted")
        raise SystemExit
