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

    def getTitle(self):
        return self._data["entityTitle"]

    def __str__(self):
        return self.getTitle()

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
        """Download all of the assignments to the directory specified."""
        mkdirAndCd(directory)

        for assignment in self.getAssignments():
            assignment.download()

        os.chdir('..')

    def downloadResources(self, directory="resources"):
        """Download all of the resources to the directory specified."""
        self.getResources().download(directory)

    def download(self):
        """Download everything that we can."""
        mkdirAndCd(self.getTitle())

        self.downloadAssignments()
        self.downloadResources()

        os.chdir('..')

    def getResources(self):
        """Get the base resources folder"""
        return BspaceFolder(self._bspace, urls.bSpaceSiteContent %
                self._data["id"], "resources - " + self.getTitle())

    def __getattribute__(self, item):
        if item == "pages":
            return self.getPages()

        if item == "assignments":
            return self.getAssignments()

        if item == "resources":
            return self.getResources()

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
    def __init__(self, bspace, data):
        """Class to represent a bSpace page"""
        self._data = data
        self._bspace = bspace

    def __str__(self):
        return self._data["title"]

class BspaceFolder(object):
    def __init__(self, bspace, url, title=""):
        self._bspace = bspace
        self._url = url
        self._title = title

    @cached
    def getItems(self):
        soup = bs(self._bspace.get(self._url).text)
        itemSoup = soup.findAll("li")

        items = []

        for itemLi in itemSoup:
            # Note: there are some empty <li> sometimes, ignore these. We are
            # only interested in "file" and "folder" class urls
            try:
                itemType = itemLi["class"][0]
                if itemType == "folder":
                    link = itemLi.find("a")
                    items.append(BspaceFolder(self._bspace, self._url +
                        link["href"], link.text))
                elif itemType == "file":
                    link = itemLi.find("a")
                    if (link["class"][0] ==
                            "org_sakaiproject_content_types_urlResource"):
                        # TODO: Resource is a URL. Deal with this...
                        pass
                    elif (link["class"][0] ==
                            "org_sakaiproject_content_types_fileUpload"):
                        items.append(BspaceFile(self._bspace, self._url +
                            link["href"], link.text, link["href"]))
                elif itemType == "upfolder":
                    # Link to previous folder, ignore
                    pass
                else:
                    print("WARNING: Unknown item type: %s, ignoring!", itemType)
            except KeyError:
                # empty <li>
                pass

        return items

    def printItems(self):
        pprint_table(sys.stdout, [('Id', 'Type', 'Title')] + [(i,
            self.items[i].getType(), self.items[i]) for i in
            range(len(self.items))])

    def download(self, folder=""):
        if folder == "":
            folder = self._title

        mkdirAndCd(folder)

        for item in self.items:
            item.download()

        os.chdir('..')


    def getType(self):
        return "Folder"

    def __iter__(self):
        return self.items

    def __getitem__(self, index):
        return self.items[index]

    def __str__(self):
        return self._title

    def __getattribute__(self, item):
        if item == "items":
            return self.getItems()

        return object.__getattribute__(self, item)

class BspaceFile(object):
    def __init__(self, bspace, url, title="", filename=""):
        self._bspace = bspace
        self._url = url
        self._title = title
        self._filename = filename

    def __str__(self):
        return self._title

    def getType(self):
        return "File"

    def download(self):
        req = self._bspace.get(self._url)
        outFile = open(self._filename, 'wb')
        outFile.write(req.content)
