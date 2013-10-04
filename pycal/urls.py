""" This file contains a list of URLs used by the various sites. All URLs should
be here to be able to update stuff easily when it changes.
"""

class urls:
    # CAS
    casLogin = "https://auth.berkeley.edu/cas/login"

    # bSpace
    bSpaceBase = "https://bspace.berkeley.edu"
    bSpaceService = bSpaceBase + "/sakai-login-tool/container"
    bSpaceUserInfo = bSpaceBase + "/direct/user/current.xml"
    bSpaceMembership = bSpaceBase + "/direct/membership.xml"
    bSpaceSiteList = bSpaceBase + "/direct/site.json"

