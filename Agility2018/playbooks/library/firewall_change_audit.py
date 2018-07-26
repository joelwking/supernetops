#!/usr/bin/env python
"""
    firewall_change_audit.py

    Copyright (c) 2018 World Wide Technology, Inc.
    All rights reserved.

    Author: Joel W. King (joel.king@wwt.com)

    Demonstration of producing an audit report of changes made to a CISCO ACL
    from audit records stored in a MongoDB

    Set environmental variables to provide input to the program.

    export DB_COLLECTION=rtp_wan_edge
    export DB_DATABASE=firewall_config
    export DB_PORT=27017
    export DB_HOST=rocket.sandbox.wwtatc.local

    Usage: python firewall_change_audit.py

    Reference: http://api.mongodb.com/python/current/tutorial.html

    Linted with flake8

    [flake8]
    max-line-length = 100
    ignore = E402

"""

from pymongo import MongoClient
import bson.objectid
import os


def generate_report(collection):
    """
       Retrieve all the documents in the 'audit' collection.
       Create a dictionary with the timestamp as the key and the document as the value.
       Sort the documents based on the timestamp.
       Print a report showing the configuration changes to the hosts over time.
    """
    all_documents = dict()
    for document in collection.find():
        key = '{}_{}'.format(document.get('iso8601'), document.get('_id'))
        all_documents[key] = document

    for timestamp in sorted(all_documents):                     # return a list of the sorted keys
        print_change_to_device(all_documents.get(timestamp))    # Print the device audit document
    return


def print_change_to_device(dad):
    """
       Print the fields from the device audit document to show
       the ACL modifications over time.
    """
    print '\n'
    print '{:15}{:10} {} _id:{}'.format(dad['config']['ansible_net_hostname'], dad['imdata']['ticket']['number'], dad['iso8601'], dad['_id'])
    print '{:25} ACL:{}'.format('', dad['imdata']['firewall']['acl_name'])
    for update in dad['updates']:
        for command in update['commands']:
            if "ip access-list" in command:
                pass
            else:
                print '{:25} {}'.format('', command)
    return


def main():
    """
       Set up the session with the MongoDB based on the values of the required environment variables
    """

    provider = dict(collection=os.environ.get('DB_COLLECTION'),
                    database=os.environ.get('DB_DATABASE'),
                    port=os.environ.get('DB_PORT'),
                    host=os.environ.get('DB_HOST'))

    try:
        client = MongoClient(provider['host'], int(provider['port']))
    except TypeError:
        client = MongoClient(provider['host'], 27017)

    db = client[provider['database']]
    collection = db[provider['collection']]

    return(generate_report(collection))


if __name__ == '__main__':
    main()
