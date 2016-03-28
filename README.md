# MeMusic
Minimalistic [eMusic](http://www.emusic.com) downloader

The official [eMusic download manager](http://www.emusic.com/info/download-manager-6/) has no Linux build available since v5 while the old v4.1.4 Linux build is obsolete and does not work anymore on recent distributions.

We provide here a basic eMusic downloader written in Python (2.7) & GTK (2) that basically does the job and nothing more...

![Snapshot of the GUI](/img/snap.png)

## Requirements

Something like packages `python2.x` and `python-gtk2`.

## Configuration

Set the path to your eMusic library at the beginning of `memusic.py`:
```
music_lib = '/home/you/path/to/eMusic/'
```

The downloads will follow the following format (which is not customisable, unless you change the `TrackDownloader.full_path` property in the code):
```
{eMusic library}/artist/album/num_title.mp3
```

## Usage

Command line download :
```
$ ./memusic.py file.emx
```

GUI download :
```
$ ./memusic-gui.py file.emx
```

You should ideally configure your browser to launch `memusic-gui.py` when opening `.emx` files.

By the way, `firefox-memusic-launcher.sh` provides a basic script to launch the command line version of MeMusic in an `xterm` window from your favorite browser (path to `memusic.py` has to be changed in the first line). GUI usage is however prefered in most cases.

Finally, eMusic uses a cookie `dlmInstalled=1` to identify the systems where the eMusic download manager is installed and thus allow the download of the `.emx` file. `eMusic_dlmInstalled.user.js` is a [Greasemonkey](https://addons.mozilla.org/en-US/firefox/addon/greasemonkey/) script that automatically creates this cookie whenever necessary (not a big deal, but one might find that useful).
