#!/usr/bin/env python3
"""
Module Docs
"""


def schools_by_topic(mongo_collection, topic):
    """
    Function
    """
    return list(mongo_collection.find({ "topics": topic }))
