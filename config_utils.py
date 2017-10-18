#!/usr/bin/env python

from storage_utils import FileStorageManager

class GoogleDriveManagerConfig(FileStorageManager):
    def __init__(self, config):
        super(GoogleDriveManagerConfig, self).__init__(config)

    def __get_name(self):
        return "Google Drive Configuration"

    def load(self):
        print("Reading %s from file %s" % (self.__get_name(), str(self.path)))
        super(GoogleDriveManagerConfig, self).load()

    def save(self):
        print("Writing %s to file %s" % (self.__get_name(), str(self.path)))
        super(GoogleDriveManagerConfig, self).save()


class LocalFileManagerConfig(FileStorageManager):
    def __init__(self, config):
        super(LocalFileManagerConfig, self).__init__(config)

    def __get_name(self):
        return "File Configuration"

    def load(self):
        print("Reading %s from file %s" % (self.__get_name(), str(self.path)))
        super(LocalFileManagerConfig, self).load()

    def save(self):
        print("Writing %s to file %s" % (self.__get_name(), str(self.path)))
        super(LocalFileManagerConfig, self).save()

class MasterConfig(FileStorageManager):
    def __init__(self, config):
        super(MasterConfig, self).__init__(config)

    def __get_name(self):
        return "Master Configuration"

    def load(self):
        print("Reading %s from file %s" % (self.__get_name(), str(self.path)))
        super(MasterConfig, self).load()

    def save(self):
        print("Writing %s to file %s" % (self.__get_name(), str(self.path)))
        super(MasterConfig, self).save()


class ConfigFactory:
    def construct(self, config, manager_type):
        if (manager_type == "master"):
            return MasterConfig(config)

        elif (manager_type == "gdrive"):
            return GoogleDriveManagerConfig(config)

        return LocalFileManagerConfig(config)
