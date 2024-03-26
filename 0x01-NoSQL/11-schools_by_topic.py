#!/usr/bin/env python3
""" Python function that changes all topics of a school document based on the name """


def schools_by_topic(mongo_collection, topic):
    """
    Python function that changes all topics of a
    school document based on the name
    """
    return list(mongo_collection.find_one({"topic": topic}))
