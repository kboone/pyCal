""" This file contains a list of URLs used by the various sites. All URLs should
be here to be able to update stuff easily when it changes.
"""

class urls:
    # CAS
    casLogin = "https://auth.berkeley.edu/cas/login"

    # bSpace
    bSpaceBase = "https://bspace.berkeley.edu"
    bSpaceService = bSpaceBase + "/sakai-login-tool/container"
    bSpaceSiteList = bSpaceBase + "/direct/site.json"
    bSpaceSitePages = bSpaceBase + "/direct/site/%s/pages.json"
    bSpaceSiteAssignments = bSpaceBase + "/direct/assignment/site/%s.json"

