import requests
import json
import logging


class saltAPI:
    def __init__(self, url, user, password, authmethod):
        self.url = url
        self.user = user
        self.password = password
        self.authmethod = authmethod
        self.getToken()
    
    def VerifyToken(self):
        """Does a very simple command against the salt master to make sure
        it's running properly and if the token is not valid or expired,
        requests a new token"""
        # Need to change this to a better call, right now only pings one
        # hard-coded hostname
        data = {"client" : "local",
            "tgt" : "cobbler",
            "fun" : "test.ping"}
        headers = {"X-Auth-Token" : self.token, 'Accept': 'application/json'}
        try:
            r = requests.post(self.url, data, headers=headers)
            if r.status_code == 401:
                self.getToken()
        except Exception as e:
            logging.error("""Exception: %s
                %s
                %s""" % (type(e), e.args, e))
            return False
    
    def getToken(self):
        """Gets an authtoken for use from salt login"""
        data = {'username': self.user,
            'password': self.password,
            'eauth': self.authmethod}
        headers = {'Accept': 'application/json'}
        try:
            r = requests.post(self.url + '/login', data, headers=headers)
            res = r.json()
            self.token = res['return'][0]['token']
            return True
        except Exception as e:
            logging.error("""Exception: %s
                %s
                %s""" % (type(e), e.args, e))
            return False

    def pingHosts(self, target):
        """Runs a salt test.ping against the given targets"""
        self.VerifyToken()
        data = {"client" : "local",
            "tgt" : target,
            "fun" : "test.ping"}
        headers = {"X-Auth-Token" : self.token, 'Accept': 'application/json'}
        try:
            r = requests.post(self.url, data, headers=headers)
            res = r.json()
            return res['return'][0]
        except Exception as e:
            logging.error("""Exception: %s
                %s
                %s""" % (type(e), e.args, e))
            return False
    
    def getVMs(self, target):
        """Gets all libvirt VMs on target(s)"""
        self.VerifyToken()
        data = {"client" : "local",
            "tgt" : target,
            "fun" : "virt.list_active_vms"}
        headers = {"X-Auth-Token" : self.token, 'Accept': 'application/json'}
        try:
            r = requests.post(self.url, data, headers=headers)
            res = r.json()
            return res['return'][0]
        except Exception as e:
            logging.error("""Exception: %s
                %s
                %s""" % (type(e), e.args, e))
            return False

    def rebootVM(self, target, vm):
        """Power cycles a VM on target via libvirt"""
        self.VerifyToken()
        data = {"client" : "local",
            "tgt" : target,
            "fun" : "virt.reset",
            "arg" : vm}
        headers = {"X-Auth-Token" : self.token, 'Accept': 'application/json'}
        try:
            r = requests.post(self.url, data, headers=headers)
            res = r.json()
            return res['return'][0]
        except Exception as e:
            logging.error("""Exception: %s
                %s
                %s""" % (type(e), e.args, e))
            return False
