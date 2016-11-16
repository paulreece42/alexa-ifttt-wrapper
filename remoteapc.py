#!/usr/bin/python

import saltAPI
from flask import Flask, request, jsonify
app = Flask(__name__)


# URL of your slack API. You should use https here for anything in prod
#
# https://docs.saltstack.com/en/latest/topics/eauth/index.html
# https://docs.saltstack.com/en/latest/ref/netapi/all/salt.netapi.rest_cherrypy.html
APIURL = 'http://192.168.1.10:8000'
APIUSER = 'salt'
APIPASS = 'tlas'

# You can set this to 'auto' but 'pam' usually works better for me. YMMV.
APIAUTH = 'pam'

# IFTTT passes this token to authenticate iteself as a very
# basic security
AUTHTOKEN = 'ChangeMeToSomethingElse' 

sa = saltAPI.saltAPI(APIURL, APIUSER, APIPASS, APIAUTH)


def getVMHost(myvm):
    """Returns the name of the hypervisor a VM lives on"""
    allVMs = sa.getVMs('compute*')
    for VM in allVMs:
        if myvm in allVMs[VM]:
            return VM



@app.route('/apc/<vmname>', methods=['POST'])
def rebootVM(vmname):
    """ Gets the name of a VM, finds out what compute note it's on
    and power-cycles it. Mostly used for my plex server when it runs
    out of RAM"""
    data = request.get_json(force=True)
    if data['token'] == AUTHTOKEN and data['action'] == "reboot":
         return jsonify(sa.rebootVM(getVMHost(vmname), vmname))


if __name__ == "__main__":
    app.run(host='0.0.0.0')
