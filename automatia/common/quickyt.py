from __future__ import unicode_literals

import re

from automatia import *
from automatia.const.priority import Gym

activated = import_exists("youtube_dl")
y_re = r'(?:youtube(?:-nocookie)?\.com/(?:[^/\n\s]+/\S+/|(?:v|e(?:mbed)?)/|\S*?[?&]v=)|youtu\.be/)([' \
       r'a-zA-Z0-9_-]{11})'


class YTModule(AutomatiaModule):
    def __init__(self):
        AutomatiaModule.__init__(self)

    def Match(self, url):
        return (re.search(y_re, url, re.I) is not None) and activated

    def Name(self):
        return "quickyt"

    def FriendlyName(self):
        if activated:
            return "QuickYT"
        else:
            return "inactive QuickYT"

    def Priority(self):
        return Gym

    def Do(self, URL):
        self.Print("Loading youtube-dl...")
        import youtube_dl

        class MyLogger(object):
            def debug(l, msg):
                # self.Print("[D]\n", msg)
                pass

            def warning(l, msg):
                self.Print("[W]", msg)

            def error(l, msg):
                self.Print("[E]", msg)

        def hook(d):
            if d["status"] == "downloading":
                self.Print("[P] {_total_bytes_str} @ {_percent_str} @ {_speed_str} ETA {_eta_str}".format(**d),
                           beginning='\r')
            elif d["status"] == "finished":
                self.Print("[P] Done @ '{filename}'".format(**d), beginning="\n")

        {u'status': u'downloading', u'downloaded_bytes': 34365079, u'_percent_str': u' 84.9%',
         u'_speed_str': u'760.85KiB/s', u'elapsed': 0.003942966461181641, u'total_bytes': 40474540,
         u'tmpfilename': u'Hart Vortex ~ Chief Justice of England - The Great Ace Attorney Music Extended-TkXIqXR5aqY.mp4.part',
         u'speed': 779108.8334744226, u'_total_bytes_str': u'38.60MiB',
         u'filename': u'Hart Vortex ~ Chief Justice of England - The Great Ace Attorney Music Extended-TkXIqXR5aqY.mp4',
         u'eta': 7, u'_eta_str': u'00:07'}

        opt = {
            'format': 'best[height<800]',
            'logger': MyLogger(),
            'progress_hooks': [hook]
        }

        yt = youtube_dl.YoutubeDL(opt)

        yt.download([URL])

        return Finish()


def a():
    return YTModule()
