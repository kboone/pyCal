from .cas import CasSite
from .external.padnums import pprint_table, pprint_list
from .urls import urls
from .utilities import cached, mkdirAndCd

from bs4 import BeautifulSoup as bs

import os
import sys


class Bspace(CasSite):
    def __init__(self):
        super().__init__(urls.bSpaceService)

    @cached
    def getSites(self):
        jsonData = self.get(urls.bSpaceSiteList).json()

        sites = []
        for siteData in jsonData["site_collection"]:
            sites.append(BspaceSite(self, siteData))

        return sites

    def printSites(self):
        pprint_list(self.sites, "Site")

    def __getattribute__(self, item):
        if item == "sites":
            return self.getSites()

        return object.__getattribute__(self, item)


class BspaceSite(object):
    def __init__(self, bspace, data):
        """Setup a class representing a bSpace site. bspace is the Bspace object
        used. data is a dict representing the site (loaded from a json dump)."""
        self._data = data
        self._bspace = bspace

    def getName(self):
        return self["entityTitle"]

    def __str__(self):
        return self._data["entityTitle"]

    def __repr__(self):
        return "BspaceSite(name='%s')" % self._data["entityTitle"]

    def __getitem__(self, item):
        return self._data[item]

    @cached
    def getPages(self):
        jsonData = self._bspace.get(urls.bSpaceSitePages %
                self._data["id"]).json()

        pages = []
        for pageData in jsonData:
            pages.append(BspacePage(self._bspace, pageData))

        return pages

    def printPages(self):
        pprint_list(self.pages, "Page")

    @cached
    def getAssignments(self):
        jsonData = self._bspace.get(urls.bSpaceSiteAssignments %
                self._data["id"]).json()

        assignments = []
        for assignmentData in jsonData["assignment_collection"]:
            assignments.append(BspaceAssignment(self._bspace, assignmentData))

        return assignments

    def printAssignments(self):
        pprint_list(self.assignments, "Assignment")

    def downloadAssignments(self, directory="assignments"):
        """Download all of the assignments to the directory specified. This
        directory will be created if it doesn't exist. Specifying an empty
        directory name or '.' will use the current directory"""
        mkdirAndCd(directory)

        for assignment in self.getAssignments():
            assignment.download()

        os.chdir('..')

    def __getattribute__(self, item):
        if item == "pages":
            return self.getPages()

        if item == "assignments":
            return self.getAssignments()

        return object.__getattribute__(self, item)



class BspaceAssignment(object):
    def __init__(self, bspace, data):
        """Class to represent a bSpace assignment"""
        self._data = data
        self._bspace = bspace

    def __str__(self):
        return self._data["title"]

    def download(self):
        for attachment in self._data["attachments"]:
            url = attachment["url"]
            req = self._bspace.get(url)

            outFile = open(attachment["name"], 'wb')
            outFile.write(req.content)


class BspacePage(object):
    # TODO: Properly interpret pages and actually let the user interact with
    # them.
    def __init__(self, bspace, data):
        """Class to represent a bSpace page"""
        self._data = data
        self._bspace = bspace

    def __str__(self):
        return self._data["title"]
