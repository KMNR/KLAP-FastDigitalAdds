"""
Digital Library Fast Add Tool.
@author <scj7t4@mst.edu>
PUBLIC DOMAIN
"""

import os
import sys
import mutagen
import json
import unicodedata
from urllib import urlencode
import webbrowser
import traceback
import re
import exceptions
import zlib

DEBUG = False
KLAP_URL = "http://klap.kmnr.org/lib/json/"

def normalize(itm):
    """
    This function removes all the funny characters and downcodes them to an
    ascii equivalent.
    """
    return unicodedata.normalize('NFKD', itm).encode('ascii', 'ignore')

def normalize_list(lst):
    """
    Calls normalize on a list of strings.
    """
    return [ normalize(x) for x in lst ]

def choose_option(option_lst):
    """
    Prints a menu of strings, lets the user pick one as a number (or a manual
    entry option, and returns the string the user selected
    """
    final_lst = list(set(option_lst))
    while 1:
        c = 1
        for item in final_lst:
            print "{}) {}".format(c,item)
            c += 1
        print "{}) Manually Set".format(c)
        try:
            choice = int(raw_input("Your Choice: "))
        except ValueError:
            print "You have to enter a number"
            continue
        if 0 < choice <= len(final_lst):
            return final_lst[choice-1]
        elif choice == len(final_lst)+1:
            inp = str(raw_input("Manual Value: "))
            inp = inp.strip()
            return inp
        else:
            print "Invalid Choice"
            continue

def wait_and_exit(msg,code=1):
    """
    Prints an error message. Waits to sys.exit program until user presses enter.
    """
    print msg
    raw_input("Press ENTER to continue")
    sys.exit(code)

def guess_title(filename):
    """
    Given a file name, guess the title based on the usual naming styles
    """
    (name,ext) = os.path.splitext(filename)
    r = re.search("([0-9]+)\W*(\w.+)",name)
    if r != None:
        # return number, title tuple
        return (r.group(1),r.group(2))
    else:
        return (None, name)
        
def open_klap(obj):
    # Code it as json
    js = json.dumps(obj)
    jsz = zlib.compress(js,9)
    # Make a query string dict
    dic = {'data':jsz,'z':1}
    # Encode it as a query string
    qs = urlencode(dic)
    # Determine target url
    final_url = "{}?{}".format(KLAP_URL,qs)
    # Open up KLAP!
    webbrowser.open_new_tab(final_url)
            
def main():
    """
    Scans a folder for music files with metadata. Collects metadata information
    from all music files and assumes they belong to the same album. Produces a
    simple description of the album that it loads into a KLAP form.
    """
    
    # Help the user
    if len(sys.argv) != 2:
        print "Usage: {} /PATH/TO/ALBUM/LOCATION".format(sys.argv[0])
        sys.exit(1)

    # Set the active directory to the one being scanned
    os.chdir(unicode(sys.argv[1]))
    path = unicode(os.getcwd())

    tracks = []
    album_names = []
    artist_names = []
    # Counter for tracks if the number metadata isn't supplied
    c = 1
    # Loop over each file in the folder
    for song in sorted(os.listdir(path)):
        fullpath = os.path.join(path,song)
        # We won't recurse and we can't do stuff with directories
        if os.path.isdir(fullpath):
            continue
        # Some debug stuff...
        print "File: {}".format(normalize(song)),
        # Mutagen lets us read the metadata
        audio = mutagen.File(fullpath,easy=True)
        if audio == None:
            print "Not Audio"
            continue
        else:
            print "Audio File"
        if DEBUG:
            print audio.pprint()
        # If it's retarded you could have a lot of artist data, so we'll
        # eventually have the user pick just one
        try:
            album_names += audio['album']
        except KeyError:
            pass
            
        try:
            artist_names += audio['artist']
            if len(audio['artist']) > 0:
                track_artist = normalize(audio['artist'][0])
            else:
                track_artist = None
        except KeyError:
            track_artist = None
            
        try:
            number = audio['tracknumber'][0].split('/')[0]
        except KeyError:
            number = None
            
        # Add it to the tracks list
        
        d = None
        try:
            title = normalize(audio['title'][0])
            # If we couldn't get a track number from the metadata we will
            # guess it with our counter.
            if number == None:
                number = c
            d = {'title': title, 'number':int(number)}
        except KeyError:
            (ntmp,title) = guess_title(song)
            if ntmp != None:
                number = ntmp
            elif number == None:
                # The filename didn't give us a number and the metadata didn't
                # Either, give up!
                wait_and_exit("I can't give this track a number, Aborting.")
            d = {'title':title, 'number':int(number)}
        if d:
            d['artist'] = track_artist
            tracks.append(d)
        
        # Increase the track number if we only have some of the data
        c += 1
    
    # If there were no tracks found assume the user made a mistake
    if len(tracks) == 0:
        wait_and_exit("Didn't find any tracks in that folder, nothing to do :(")
    
    # Make sure the info is safe for KLAP
    artist = normalize_list(artist_names)
    album = normalize_list(album_names)
    
    print "\n-----------------------------\n"
    
    # Let the user pick the single album title and artist
    print "Please choose the artist:"
    artist = choose_option(artist)
    print "Please Choose The Album Name:"
    album = choose_option(album)
    
    print "\n-----------------------------\n"
    
    # Remove the artist key if it is the same as the album artist.
    for track in tracks:
        if track['artist'] == artist:
            del track['artist']
            
    # Make the dict
    obj = {'artist': artist,
           'album': album,
           'tracks': tracks,
          }
          
    open_klap(obj)

if __name__ == "__main__":
    try:
        main()
    except exceptions.SystemExit:
        raise
    except:
        print "Unexpected error:", sys.exc_info()[0]
        traceback.print_exc()
        wait_and_exit("Please take a screenshot and e-mail it to engineering@kmnr.org")