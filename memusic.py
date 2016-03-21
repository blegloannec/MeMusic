#!/usr/bin/env python

import sys, os, urllib
import os.path as path
import xml.dom.minidom as dom

music_lib = '/home/bastien/Musique/eMusic/'

class TrackDownloader:
    @staticmethod
    def get_txtnode(track, tag):
        return track.getElementsByTagName(tag)[0].firstChild.data

    @staticmethod
    def protect(str):
        return str.replace('/','_')

    def progress(self, count, blockSize, totalSize):
        pc = int(count*blockSize*100/totalSize)
        sys.stdout.write('\rDownloading %s... %d%%' % (self.file_name,pc))
        sys.stdout.flush()
    
    def __init__(self, track):
        self.artist = TrackDownloader.protect(TrackDownloader.get_txtnode(track,'ARTIST'))
        self.album = TrackDownloader.protect(TrackDownloader.get_txtnode(track,'ALBUM'))
        self.num = int(TrackDownloader.get_txtnode(track,'TRACKNUM'))
        self.title = TrackDownloader.protect(TrackDownloader.get_txtnode(track,'TITLE'))
        self.url = TrackDownloader.get_txtnode(track,'TRACKURL')
        self.url_art = TrackDownloader.get_txtnode(track,'ALBUMARTLARGE')
        self.file_name = '%d_%s.mp3' % (self.num,self.title)
        self.artist_path = path.join(music_lib,self.artist)
        self.album_path = path.join(self.artist_path,self.album)
        self.full_path = path.join(self.album_path,self.file_name)
        self.art_path = path.join(self.album_path,'Folder.jpg')
        
    def download(self, progress_call=None):
        try:
            os.mkdir(self.artist_path)
            print 'Info: %s created' % self.artist_path
        except:
            pass
        try:
            os.mkdir(self.album_path)
            print 'Info: %s created' % self.album_path
        except:
            pass
        if not path.isfile(self.art_path):
            urllib.urlretrieve(self.url_art,self.art_path)
            print 'Info: album art downloaded'
        sys.stdout.flush()
        urllib.urlretrieve(self.url,self.full_path,reporthook=(self.progress if progress_call==None else progress_call))
        if progress_call==None:
            print '\rDownloading %s... done' % self.file_name


class eMusicDownloader:
    def __init__(self, emx_file):
        self.emx_file = emx_file
        try:
            self.emx_dom = dom.parse(self.emx_file)
        except:
            print >> sys.stderr, 'EMX file error!'
            sys.exit(1)
        self.tracks = [TrackDownloader(t) for t in self.emx_dom.getElementsByTagName('TRACK')]
        self.nb_tracks = len(self.tracks)

    def read_emx(self):
        f = open(self.emx_file,'r')
        emx = f.read()
        f.close()
        return emx
        
    def download(self):
        for t in self.tracks:
            t.download()


## MAIN
def console_main():
    if len(sys.argv)!=2:
        print >> sys.stderr, 'usage: %s file.emx' % sys.argv[0]
        sys.exit(1)
    EMD = eMusicDownloader(sys.argv[1])
    EMD.download()

if __name__ == '__main__':
    console_main()
