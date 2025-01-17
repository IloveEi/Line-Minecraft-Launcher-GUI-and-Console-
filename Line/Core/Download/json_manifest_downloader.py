from requests import get
from json import loads
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QThread

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import host_provider


class LJsonManifestDownload(QThread):

    finished = pyqtSignal(dict)

    def __init__(self, src):
        super().__init__()
        self.src = src
        self.official_hosts = host_provider.LOfficialHosts()

    def run(self):
        if self.src == "BmclApi":
            provider = host_provider.LBmclApiSource()
        elif self.src == "LineMirror":
            provider = host_provider.LLineMirrorSource()
        else:
            provider = host_provider.LOfficialSource()
        versionManifest = loads(
            get(provider.versionsManifest).text
        )
                    
        if self.src != "Official":
            for i in versionManifest["versions"]:
                i["url"] = host_provider.LPiston(i["url"]).replace(provider.hostsProvider.piston.getPiston())
            self.finished.emit(versionManifest)
        else:
            self.finished.emit(versionManifest)