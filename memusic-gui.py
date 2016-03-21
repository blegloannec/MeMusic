#!/usr/bin/env python

import sys, threading
from memusic import eMusicDownloader
import pygtk
pygtk.require('2.0')
import gtk, gobject

# Crucial for threads to work with GTK:
gobject.threads_init()

class eMusicDownloaderGUI(gtk.Window):
    def __init__(self, downloader):
        gtk.Window.__init__(self)
        self.downloader = downloader
        self.connect('destroy', gtk.main_quit)
        self.set_title('memusic')
        self.set_default_size(600,440)
        self.set_border_width(5)
        self.layout = gtk.Table(2,1,False)
        self.layout.set_row_spacings(5)
        self.layout.set_border_width(5)
        self.add(self.layout)
        
        self.notebook = gtk.Notebook()
        self.layout.attach(self.notebook,0,1,0,1)

        self.dl_window = gtk.ScrolledWindow()
        self.dl_list = gtk.ListStore(gobject.TYPE_INT,gobject.TYPE_STRING,gobject.TYPE_INT)
        self.dl_view = gtk.TreeView(self.dl_list)
        self.dl_col_no = gtk.TreeViewColumn('No',gtk.CellRendererText(),text=0)
        self.dl_col_no.set_resizable(True)
        self.dl_view.append_column(self.dl_col_no)
        #self.dl_col_no.add_attribute(self.dl_col_no_renderer,'text',0)
        self.dl_col_title = gtk.TreeViewColumn('Title',gtk.CellRendererText(),text=1)
        self.dl_col_title.set_resizable(True)
        self.dl_view.append_column(self.dl_col_title)
        self.dl_col_progress = gtk.TreeViewColumn('Progress',gtk.CellRendererProgress(),value=2)
        self.dl_view.append_column(self.dl_col_progress)
        self.dl_window.add(self.dl_view)
        self.notebook.append_page(self.dl_window,gtk.Label('Downloads'))
        
        self.emx_window = gtk.ScrolledWindow()
        self.emx_view = gtk.TextView()
        self.emx_window.add(self.emx_view)
        self.emx_view.set_editable(False)
        self.emx_view.get_buffer().set_text(self.downloader.read_emx())
        self.notebook.append_page(self.emx_window,gtk.Label('EMX file'))
        
        self.bclose = gtk.Button()
        self.bclose_label = gtk.Label('Close')
        self.bclose_label.set_padding(10,5)
        self.bclose.add(self.bclose_label)
        self.bclose.set_sensitive(False)
        self.bclose_layout = gtk.HBox()
        self.layout.attach(self.bclose_layout,0,1,1,2,yoptions=gtk.SHRINK)
        self.bclose_layout.pack_end(self.bclose,False,False)
        self.bclose.connect_object('clicked', gtk.Widget.destroy, self)
        
        for t in self.downloader.tracks:
            self.dl_list.append((t.num,t.title,0))
        
        self.show_all()
        self.dl_thread = threading.Thread(target=self.download)

    def set_progress(self, row, pc):
        self.dl_list.set_value(self.dl_list.get_iter(row),2,pc)

    def progress(self, row, count, blockSize, totalSize):
        pc = int(count*blockSize*100/totalSize)
        gobject.idle_add(self.set_progress,row,pc)
        
    def download(self):
        for i in range(self.downloader.nb_tracks):
            self.downloader.tracks[i].download(lambda x,y,z: self.progress(i,x,y,z))
        gobject.idle_add(self.bclose.set_sensitive,True)
        
    def main(self):
        self.dl_thread.start()
        gtk.main()


## MAIN
def main():
    if len(sys.argv)!=2:
        print >> sys.stderr, 'usage: %s file.emx' % sys.argv[0]
        sys.exit(1)
    GUI = eMusicDownloaderGUI(eMusicDownloader(sys.argv[1]))
    GUI.main()

if __name__ == '__main__':
    main()
