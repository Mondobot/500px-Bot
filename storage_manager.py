#!/usr/bin/env python

class StorageManager(object):
    def __init__(self, config):
        self.__config = config

    def getConfig(self):
        return self.__config

    def load(self):
        print("Saving values for StorageUtils is not implemented")

    def save(self):
        print("Saving values for StorageUtils is not implemented")
