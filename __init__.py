# -*- coding: utf-8 -*-

"""Get Google suggestions"""
import os
import time

import requests
from albertv0 import *
from lxml import html

__iid__ = "PythonInterface/v0.2"
__prettyname__ = "DeHet"
__version__ = "0.1"
__trigger__ = "dehet "
__author__ = "David Britt"
__dependencies__ = ['lxml', 'requests']

iconPath = iconLookup('google_suggest')
if not iconPath: iconPath = os.path.dirname(__file__) + "/lidwoord.png"
baseurl = 'https://www.welklidwoord.nl/{}'
user_agent = "Mozilla/5.0"


def initialize():
    global baseurl


def handleQuery(query):
    if query.isTriggered:

        stripped = query.string.strip()
        if stripped:
            time.sleep(0.25)
            if not query.isValid:
                return

            try:
                page = requests.get(baseurl.format(stripped), headers={'User-Agent': user_agent})
                tree = html.fromstring(page.content)
                lidwoord = tree.xpath("//h1/span/text()")[0]

                if lidwoord == "De of het":
                    return Item(
                        id=__prettyname__,
                        icon=iconPath,
                        text="Helaas, probeer nog een keer.",
                        subtext='Is het wel een zelfstandig naamwoord?.',
                        actions=[UrlAction('Open in welklidwoord.nl', baseurl)]
                    )
                else:
                    return Item(
                        id=__prettyname__,
                        icon=iconPath,
                        text="{} {}".format(lidwoord, stripped),
                        subtext='Druk modifier key.',
                        completion=stripped,
                        actions=[
                            UrlAction('Open in welklidwoord.nl', baseurl.format(stripped)),
                            ClipAction('Kopieer naar klipbord.', "{} {}".format(lidwoord, stripped))
                        ])
            except:
                return Item(
                    id=__prettyname__,
                    icon=iconPath,
                    text="Er is een fout opgetreden, probeer opnieuw."
                )
        else:
            return Item(id=__prettyname__,
                        icon=iconPath,
                        text="Zoek het lidwoord.",
                        subtext="dehet <woord>."
                        )
