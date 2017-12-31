from __future__ import unicode_literals

import re

from automatia import *
from automatia.const.priority import Gym
from automatia.reflect import *

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
        self.Print("Loaded youtube-dl")

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
                           beginning='\r', end=' ')
            elif d["status"] == "finished":
                self.Print("[P] Done @ '{filename}'".format(**d), beginning="\n")

        opt = {
            'format': 'best[height<800]',
            'logger': MyLogger(),
            'progress_hooks': [hook]
        }

        if HasNextArg():
            r = SimpleQuery("Choose", "do")

            if r == DOWN:
                pass
            elif r == OTHER:
                Inform("Chosen Other")
                r = StringQuery("Choose other", {"mp3": "Download mp3 version of video"})

                if r == "mp3":
                    Inform("Chosen mp3")
                    opt.update(
                        {'format': 'bestaudio/best',
                         'postprocessors': [{
                             'key': 'FFmpegExtractAudio',
                             'preferredcodec': 'mp3',
                             'preferredquality': '192',
                         }]}
                    )
            else:
                print(r)

        yt = youtube_dl.YoutubeDL(opt)

        yt.download([URL])

        return Finish()


def a():
    return YTModule()
