#!/usr/bin/env python3
"""
Module Docs
"""


def insert_school(mongo_collection, **kwargs):
    """
    Function Doc
    """
    return mongo_collection.insert_one(kwargs).inserted_id
