from __future__ import print_function
from inspect import isdatadescriptor

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']


def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('drive', 'v3', credentials=creds)

        # Call the Drive v3 API, page token max value is 1000
        storeData = {}  # nested dictionary, id is key, value is dict with name, lastModified user
        results = service.files().list(driveId="0ALT8V7p0m5I5Uk9PVA", includeItemsFromAllDrives=True, corpora="drive", supportsAllDrives=True, pageSize=1, fields="nextPageToken, files(id, name)").execute()  # page token max value is 1000

        # stuff that gets last modified user
        items = results.get('files', [])
        if not items:
            print('No files found.')
            return

        for item in items:
            # print(u'{0} ({1})'.format(item['name'], item['id']))    #prints file name and id
            i = service.files().get(fileId=item['id'], supportsAllDrives=True,
                                    fields="lastModifyingUser").execute()  # gets last modified user
            print(item["name"])
            nP = results["nextPageToken"]
            print(nP)
            results = service.files().list(
                driveId="0ALT8V7p0m5I5Uk9PVA", includeItemsFromAllDrives=True, corpora="drive", supportsAllDrives=True, pageSize=1, pageToken = nP, fields="nextPageToken, files(id, name)").execute()  # page token max value is 1000
            it = results.get('files', [])
            print(it[0]["name"])
            if item["id"] not in storeData:
                storeData[item["id"]] = {
                    "name": item["name"], "lastModified": i["lastModifyingUser"]["displayName"]}

        pagetoken = service.changes().getStartPageToken(driveId="0ALT8V7p0m5I5Uk9PVA",supportsAllDrives=True).execute()
        pagetoken = pagetoken.get("startPageToken")
        #print(pagetoken)
        #pagetoken stuff
            
    except HttpError as error:
    # TODO(developer) - Handle errors from drive API.
            print(f'An error occurred: {error}')

    #allFiles = storeData.keys()
    #print(allFiles)
    #print(len(allFiles))



if __name__ == '__main__':
    main()


# divisions = {
#     "mechanical": "#mechanical",
#     "electrical": "#electrical",
#     "software": "#software",
#     "business": "#business",
#     "marketing": "#marketing",
# }

# cycles = {
#     "aevum": "#aevum",
#     "novum": "#novum",


# Database:
# FileID Division FileName Cycle
