#!/usr/bin/env python3
""" Python function that lists all documents in a collection """


def insert_school(mongo_collection, **kwargs):
    return mongo_collection.insert(kwargs)
