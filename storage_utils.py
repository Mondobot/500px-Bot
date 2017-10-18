#!/usr/bin/env python

from __future__ import print_function
import json
from collections import namedtuple
from pprint import pprint
from googleapiclient import discovery
import httplib2
import os
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

from storage_manager import StorageManager

class GoogleDriveStorageManager(StorageManager):
    def __init__(self, config):
        super(GoogleDriveStorageManager, self).__init__(config)
        self.__config = config
        try:
            import argparse
            flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
        except ImportError:
            flags = None

        credentials = self.__get_credentials()
        self.__service = discovery.build('sheets', 'v4', credentials=credentials)

    def getConfig(self):
        return self.__config

    def __get_credentials(self):
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        SCOPES = self.__config.scopes#'https://www.googleapis.com/auth/spreadsheets'
        CLIENT_SECRET_FILE = self.__config.client_secret_file#'client_secret.json'
        APPLICATION_NAME = self.__config.application_name#'500px-bot'

        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'sheets.googleapis.com-python-quickstart.json')

        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else: # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)

        return credentials

    def __create_spreadsheet(self, service):
        spreadsheet_body = {
            "properties" : {
                "title" : self.__config.sheet_title
            }
        }
        request = self.__service.spreadsheets().create(body=spreadsheet_body)
        response = request.execute()


        print("Created data spreadsheed at %s" % response['spreadsheetUrl'])

        return response['spreadsheetId']

    def __get_raw_values(self, service, spreadsheet_id):
        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id, range='Sheet1!A2:C').execute()
        values = result.get('values', [])

        return values

    def load(self):
        values = []

        if self.__config.spreadsheet_id == "":
            new_spreadsheet_id = self.__create_spreadsheet(self.__service)
            self.__config = self.__config._replace(spreadsheet_id=new_spreadsheet_id)

        else:
            values = self.__get_raw_values(self.__service, self.__config.spreadsheet_id)

        return values

    def save(self, items):
        values = []
        values.extend(items)

        body = {
            "values" : values
        }

        #Clear the spreadsheet
        result = self.__service.spreadsheets().values().clear(
            spreadsheetId=self.__config.spreadsheet_id, body={},
            range="Sheet1!A:ZZ").execute()

        result = self.__service.spreadsheets().values().append(
            spreadsheetId=self.__config.spreadsheet_id, range="Sheet1!A:ZZ",
            valueInputOption="RAW", body=body).execute()

class FileStorageManager(StorageManager):
    def __init__(self, config):
        super(FileStorageManager, self).__init__(config)
        self.path = config.path
        self.data = {}

    def __get_name(self):
        return "Plain File Storage Manager"


    def __to_json(self):
        return json.dumps(self.data._asdict(), default = lambda o: o.__dict__,
                                            sort_keys=True, indent=4)

    def __load_from_json(self, json_str):
        self.data = json.loads(json_str, object_hook=lambda d: namedtuple('X',
                                                        d.keys())(*d.values()))
    def load(self):
        file = open(self.path, "r")
        self.__load_from_json(file.read())
        file.close()

    def save(self):
        file = open(self.path, "w")
        file.write(self.__to_json())
        file.close()

class StorageManagerFactory:
    def construct(self, config, manager_type):
        if (manager_type == "gdrive"):
            return GoogleDriveStorageUtils(config)

        return FileStorageManager(config)
