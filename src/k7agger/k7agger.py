'''
Created on 19/01/2011

@author: Patrick
'''
from mutagen.mp3 import MP3 # mp3 tagging support
import os, sys
import types
from operator import eq

media_types = ["mp3", "flac", "mp4", "wma"]



class StandardIterator():
    def __init__(self, items):
        self.current = 0
        self.items = items
        
    def __iter__(self):
        return self
        
    def next(self):
        if self.current < len(self.items):
            val = self.items[self.current]
            self.current += 1
            return val
        
        else:
            raise StopIteration() 


def media_type(fname):
    "returns MP3, FLAC, etc. depending on type discovered"
    #TODO: add attempt to actually parse/open the media type for confirmation\
    fname_clean = fname.strip().lower()
    if len(fname_clean) > 4 and fname_clean[-4:] == ".mp3":
        return "MP3"
    
    #nothing found ...
    return ""



class Artist():
    
    def init_members(self):
        self.path = ""
        self.artist_name = ""
        self.songs = [] # fullpath to song mp3
        self.genres = dict() # {"genre" : #songs}
        self.good_looking_dir_structure = False
        
    def __init__(self, path, artist_name = None):
        self.init_members()
        self.path = path
        self.artist_name = artist_name
        if self.artist_name == None:
            self.artist_name = path # TODO:
    
    def parse(self):
        parse_result = dict()
        self.find_all_songs()

        parse_result["dir_structure"] = self.dir_structure_needs_fixing()
        parse_result["genres"] = self.genres_needs_fixing()
        
        return parse_result
        
    def find_all_songs(self):
        dirs = [self.path]
        in_toplevel_dir = True
        # recurse down directories
        while len(dirs) > 0:
            dirname = dirs.pop()
            files = os.listdir(dirname)
            
            # foreach file in this directory
            for fname in files:
                if os.path.isdir(dirname + os.sep + fname):
                    dirs.append(dirname + os.sep + fname)
                    
                elif media_type(dirname + os.sep + fname) == "MP3":
                    try:
                        mp3song = MP3(dirname + os.sep + fname)
                        self.songs.append((dirname , fname))
                        genre = str(mp3song["TCON"])
                        if genre in self.genres:
                            self.genres[genre] += 1
                        else:
                            self.genres[genre] = 1
                            
                        #(optimized by putting this here)
                        # if there are songs in a sub-directory: its good 
                        if not in_toplevel_dir:
                            self.good_looking_dir_structure = True
                        
                    except Exception, e:
                        continue
            # next directory ...
            in_toplevel_dir = False
                
    def parse_song_genres(self):
        self.genres.clear()
        
        for song in self.songs:
            fullpath = song[0] + os.sep + song[1]
            try:
                mp3song = MP3(fullpath)
                #print "\t", mp3song["TCON"]
                genre = str(mp3song["TCON"])
                if genre in self.genres:
                    self.genres[genre] += 1
                else:
                    self.genres[genre] = 1
            except Exception, e:
                #print "Error reading: ", fullpath
                self.songs.remove(song)
        for genre in self.genres:
            #print "\t", genre, " = ", (self.genres[genre]  * 100.0)/len(self.songs), "%"
            pass
        
    # TODO:
    def __repr__(self):
        ret = self.artist_name
        return ret
    
    def dir_structure_needs_fixing(self):
        return not self.good_looking_dir_structure

    def genres_needs_fixing(self):
        threshold = 0.99
        found_threshold = False
        for genre in self.genres:
            if self.genres[genre] * 1.0 / len(self.songs) >= threshold:
                found_threshold = True
                break
            
        return (len(self.songs) > 0) and (not found_threshold)
    

class MusicCollection():
    def __init__(self, dirpath=""):
        self.artists = []
        self.conditions = ["genre"]
        self.dirpath = dirpath
        
    def parse_collection(self, dirpath=None):
        del self.artists[:]
        if not dirpath == None and len(dirpath) > 0:
            print "setting collection directory path to: ", dirpath
            self.dirpath = dirpath
            
        if (dirpath == None or len(dirpath) <= 0) and len(self.dirpath) <= 0:
            print "Error: no directory path given"
            return
        
        print "parsing ", self.dirpath
        
        for dir in os.listdir(self.dirpath):
            if os.path.isdir(self.dirpath + os.sep + dir):
                self.artists.append(Artist(self.dirpath + os.sep + dir, dir))
        for artist in self.artists:
            print artist.artist_name
            artist.parse()
            
    
    def find_artists(self, condition):
        " condition = {tag_type : value} "
        select = ""
        val = []
        
        matches = []
        
        if isinstance(condition, dict):
            select = condition.keys()[0]
            if isinstance(condition[select], list):
                val.extend(condition[select])
            else:
                val = [condition[select]]
                
        elif isinstance(condition, tuple):
            select = condition[0]
            if isinstance(condition[1], list):
                val.extend(condition[1])
            else:
                val = [condition[1]]
                
        else:
            print "unknown given"
            return
        
        #print "looking for ", val, " in ", select
        
        for artist in self.artists:
            artist_done = False
            #print artist
            for genre in artist.genres:
                #print "\t", genre
                for testval in val:
                    #print "\t\t", testval
                    #print "looking for ", testval, " in ", genre
                    if genre.find(testval) >= 0:
                        #print genre, " : ", testval
                        #print "\t\t\tfound match"
                        matches.append(artist) # remember: copies only references
                        artist_done = True
                        break
                if artist_done:
                    break
                    
        new_collection = MusicCollection(self.dirpath)
        new_collection.artists = matches
        return new_collection
    
    def __iter__(self):
        return StandardIterator(self.artists)
    
def parse_outer_directory(dirpath):
    # remove any trailing separator from dirpath
    #dirpath = dirpath.strip()
    dirpath = "E:\\MUSIC_TEST"
    
    if dirpath[:-1] == os.sep:
        dirpath = dirpath[:-1]
    
    collection = MusicCollection()
    collection.parse_collection(dirpath)
    
    print "\n matches:\n---------" 
    for artist in collection.find_artists(("genre", ["metal", "metal nu"])):
        print artist
        
    print "\n matches:\n---------" 
    for artist in collection.find_artists(("genre", ["progressive"])):
        print artist
        
    new_col = collection.find_artists(("genre", ["rock"]))
    new_col.parse_collection()
    
    print "\n matches:\n---------" 
    for artist in collection.find_artists(("genre", ["metal", "metal nu"])):
        print artist
        
    '''    
    for artist in artists:
        p_result = artist.parse()
        
        if p_result["dir_structure"] or p_result["genres"]:
            print artist.artist_name
            
        if p_result["dir_structure"]:
            print "\t - Directory structure needs fixing"
        if p_result["genres"]:
            print "\t - Genres need fixing"    
    '''