#!/usr/bin/env python3
"""
Module Docs
"""
from pymongo import MongoClient


client = MongoClient('mongodb://localhost:27017')
nginx_collection = client.logs.nginx

num_logs = nginx_collection.count_documents({})

methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
num_methods = {}

for method in methods:
    num_methods[method] = nginx_collection.count_documents({"method": method})

num_docs = nginx_collection.count_documents(
    {"method": "GET", "path": "/status"})

print(f"{num_logs} logs\
    Methods:\
        method GET: {num_methods.get('GET')}\
        method POST: {num_methods.get('POST')}\
        method PUT: {num_methods.get('PUT')}\
        method PATCH: {num_methods.get('PATCH')}\
        method DELETE: {num_methods.get('DELETE')}\
    {num_docs} status check")
