#!/usr/bin/env python3
"""
Module Docs
"""


def update_topics(mongo_collection, name, topics):
    """
    Function Docs
    """
    mongo_collection.update_many({"name": name}, {"$set": {"topics": topics}})
