#!/usr/bin/env python3
""" Python function that lists all documents in a collection """


def insert_school(mongo_collection, **kwargs):
    document = {}
    for key, value in kwargs.items():
        document[key] = value
    return mongo_collection.insert(document)
