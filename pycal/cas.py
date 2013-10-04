from getpass import getpass
import requests as req
from bs4 import BeautifulSoup as bs

from .urls import urls
from .config import config


def request(reqName):
    """Decorator generator to properly handle requests and to debug them name is
    the HTML request name (eg: GET) which is used for debug purposes."""
    def decorator(func):
        def wrapped(self, url, *args, **kwargs):
            try:
                if config.debugPrintRequests:
                    print(reqName + ": " + url)
            except AttributeError:
                pass
        
            kwargs["cookies"] = self._cookies
            return func(self, url, *args, **kwargs)
        return wrapped
    return decorator


class CasSite(object):
    """Base class to access a website using the Calnet Central Authentication
    Service.
    
    This handles logging in through the CAS system, cookies and basic page
    requests. It will ask for a username and password if one isn't specified in
    the config file.
        
    This is a virtual class, and the serviceUrl must be specified for any
    non-virtual subclass. This is the URL used as a redirect in the CAS login.
    """
    def __init__(self, serviceUrl):
        self.login(serviceUrl)


    def login(self, serviceUrl):
        """ Log in to a service using through CAS"""

        # the username and password can be specified in the config file, or
        # prompted for        
        try:
            username = config.username
        except AttributeError:
            username = input("Username: ")
        
        try:
            password = config.password
        except AttributeError:
            password = getpass()

        params = {
                "service" : serviceUrl,
        }
        post = {
                "username" : username,
                "password" : password,
        }

        # Get a conversation ID. This is stored in the lt variable of the login
        # form
        casPage = req.get(urls.casLogin, params=params)
        convId = bs(casPage.text).find("input", {"name":"lt"})["value"]

        # Log in using that conversation ID
        post["lt"] = convId
        post["_eventId"] = "submit"
        loginPage = req.post(urls.casLogin, params=params, data=post)

        # Save the cookies so that we can continue browsing. These get lost in
        # the redirects for some sites. Search backwards and find the last
        # cookies that were used.
        if loginPage.cookies:
            self._cookies = loginPage.cookies
        else:
            for page in reversed(loginPage.history):
                if page.cookies:
                    self._cookies = page.cookies
                    break

    @request("GET")
    def get(self, url, *args, **kwargs):
        return req.get(url, *args, **kwargs)

    @request("POST")
    def post(self, url, *args, **kwargs):
        return req.post(url, *args, **kwargs)

    @request("PUT")
    def put(self, url, *args, **kwargs):
        return req.put(url, *args, **kwargs)

    @request("DELETE")
    def delete(self, url, *args, **kwargs):
        return req.delete(url, *args, **kwargs)

    @request("HEAD")
    def head(self, url, *args, **kwargs):
        return req.head(url, *args, **kwargs)

    @request("OPTIONS")
    def options(self, url, *args, **kwargs):
        return req.options(url, *args, **kwargs)
