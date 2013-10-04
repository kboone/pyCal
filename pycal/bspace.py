from .cas import CasSite
from .external.padnums import pprint_table
from .urls import urls
from .utilities import cached

from bs4 import BeautifulSoup as bs

import json
import sys


class Bspace(CasSite):
    def __init__(self):
        super().__init__(urls.bSpaceService)

    @cached
    def getSites(self):
        siteReq = self.get(urls.bSpaceSiteList)
        jsonData = json.loads(siteReq.text)

        sites = []
        for siteData in jsonData["site_collection"]:
            sites.append(BspaceSite(self, siteData))

        return sites

    def printSites(self):
        pprint_table(sys.stdout, [('Id', 'Site')] + [(i, self._sites[i]) for
            i in range(len(self._sites))])

    def __getattribute__(self, item):
        if item == "_sites":
            return self.getSites()

        return object.__getattribute__(self, item)


class BspaceSite(object):
    def __init__(self, bspace, data):
        """Setup a class representing a bSpace site. bspace is the Bspace object
        used. data is a dict representing the site (loaded from a json dump)."""
        self._data = data

    def getName(self):
        return self["entityTitle"]

    def __str__(self):
        return self._data["entityTitle"]

    def __repr__(self):
        return "BspaceSite(name='%s')" % self._data["entityTitle"]

    def __getitem__(self, item):
        return self._data[item]
