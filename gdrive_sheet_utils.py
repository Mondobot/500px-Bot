#!/usr/bin/env python

from __future__ import print_function

from pprint import pprint
from googleapiclient import discovery

import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

class StorageUtils:
    def __init__(self, config):
        self.__config = config
        pass

    def loadValues(self):
        print("Saving values for StorageUtils is not implemented")

    def saveValues(self):
        print("Saving values for StorageUtils is not implemented")
        pass


class GoogleDriveStorageUtils(StorageUtils):
    def __init__(self, config):
        super().__init__(config)

        try:
            import argparse
            flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
        except ImportError:
            flags = None

        credentials = self.__get_credentials()
        self.__service = discovery.build('sheets', 'v4', credentials=credentials)

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

    def __create_spreadsheet(self, service, credentials):
        spreadsheet_body = {
            "properties" : {
                "title" : self.__config.sheet_title
            }
        }
        request = self.__service.spreadsheets().create(body=spreadsheet_body)
        response = request.execute()

        print("Created data spreadsheed at %s" % response['spreadsheetUrl'])

        return response['spreadsheetId']

    def __get_raw_values(self, service):
        result = self.__service.spreadsheets().values().get(
            spreadsheetId=spreadsheetId, range="Sheet1").execute()
        values = result.get('values', [])

        return values

    def __parse_values(value):
        pending_follow = []
        blacklisted_follow = []

        for row in values:
            if row[4] == "pending":
                pending_follow.append(row[0])

            else:
                blacklisted_follow.append(row[0])

        return (pending_follow, blacklisted_follow)

    def loadValues(self):
        service = discovery.build('sheets', 'v4', credentials=credentials)
        values = get_values(spreadsheetId, service)

        if not values:
            create_spreadsheet(service, credentials)
            values = []

        return self.__parse_values(values)

    def saveValues(self, pending_follow, blacklisted_follow):
        values = []

        for follower in pending_follow:
            values.append([follower, int(time.time()), "pending"])

        for follower in blacklisted_follow:
            values.append([follower, int(time.time()), "blacklisted"])

        body = {
            "values" : values
        }

        result = self.__service.spreadsheets().values().append(
            spredsheetId=self.__config.spredsheetId, range="Sheet1",
            valueInputOption="RAW", body=body).execute()

def main():
    pass

if __name__ == '__main__':
    main()
