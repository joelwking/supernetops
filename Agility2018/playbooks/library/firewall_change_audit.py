


# http://api.mongodb.com/python/current/tutorial.html

from pymongo import MongoClient
import bson.objectid
import difflib

#
# firewall_config.rtp_wan_edge
#
client = MongoClient('rocket.sandbox.wwtatc.local', 27017)
db = client['firewall_config']
collection = db['rtp_wan_edge']
#
#
all_documents = dict()
for document in collection.find():
    all_documents[document.get('iso8601')] = document
    

for item in sorted(all_documents):
    change_request = all_documents.get(item)
    print "%s %s" % (change_request['imdata']['ticket']['number'], item)
    print '{:35} {}{}'.format(change_request['config']['ansible_net_hostname'], "ACL:", change_request['imdata']['firewall']['acl_name'])
    for update in change_request['updates']:
        for command in update['commands']:
            if "ip access-list" in command:
                pass
            else:
                print '{:35} {}'.format(' ', command)

