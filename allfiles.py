from __future__ import print_function
from inspect import isdatadescriptor
import os.path

import database
import asyncio
import logging 
import logging.handlers

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

async def dtbase(id, name):
    db = database.Database()
    await db.connect()
    data = {
        "FileID": id,
        "Division": "xxx",
        "FileName": name,
        "Cycle": "xxx",
        "OldData": True,
    }
    await db.createEntry(data)
    
# async def clear():
#     db = database.Database()
#     await db.connect()
#     await db.clear_database()clear
    
    
def main():
    #clear()
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
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
        #clear()
        # Call the Drive v3 API, page token max value is 1000
        db = database.Database()
        #asyncio.run(db.clear_database())
        #asyncio.run(db.clear_database(), debug = True)
        #logging.basicConfig(level = logging.DEBUG)
        #db.clear_database()
        results = service.files().list(driveId="0ALT8V7p0m5I5Uk9PVA", includeItemsFromAllDrives=True, corpora="drive", supportsAllDrives=True, pageSize=1, fields="nextPageToken, files(id, name)").execute()  # page token max value is 1000
        # stuff that gets last modified user
        items = results.get('files', [])
        if not items:
            print('No files found.')
            return
        #db.createEntry(datat);
        asyncio.run(dtbase(items[0]["id"], items[0]["name"]))
        np = results.get('nextPageToken', None)
        for i in range(150):
            results = service.files().list(
                driveId="0ALT8V7p0m5I5Uk9PVA", includeItemsFromAllDrives=True, corpora="drive", supportsAllDrives=True, pageSize=1000, pageToken = np, fields="nextPageToken, files(id, name)").execute()  # page token max value is 1000
            it = results.get('files', [])
            np = results.get('nextPageToken', None)
            for j in it:
               if ((j["name"].find("HEIC") == -1) and  (j["name"].find("jpg") == -1)):
                   #db.createEntry(data);
                   asyncio.run(dtbase(j["id"], j["name"]))

            
        #pagetoken = service.changes().getStartPageToken(driveId="0ALT8V7p0m5I5Uk9PVA",supportsAllDrives=True).execute()
        #pagetoken = pagetoken.get("startPageToken")
        #print(pagetoken)
        #pagetoken stuff
        #print(len(allfiles))
        #print(allfiles[0:10])
        #print(len(allfiles))
        #print(allfiles[0:10])
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
