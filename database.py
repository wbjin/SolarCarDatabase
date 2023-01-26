import asyncio
from prisma import Prisma

# Prisma Database Implementation for Solar Car Drive API project

#Initialize with Database(), immediately call connect() to connect to database
#Call disconnect() to disconnect from database


# db = Database()
# db.connect()

# data = {
#     "FileID": id,
#     "Division": "",
#     "FileName": name,
#     "Cycle": "",
#     "OldData": "true",
# }
# db.createEntry(data)

class Database:
    def __init__(self):
        self.db = None

    def __del__(self):
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                loop.create_task(self.session.disconnect())
            else:
                loop.run_until_complete(self.session.disconnect())
        except Exception:
            pass

    # Connect to the database
    async def connect(self):
        self.db = Prisma()
        await self.db.connect()


    # Disconnect from the database
    async def disconnect(self):
        await self.db.disconnect()

    # Get all entries in the database
    async def get_files(self):
        users = await self.db.file.find_many()
        return users

    async def get_file(self, file_id):
        user = await self.db.users.find_first(where={'FileID': file_id,})
        return user

    async def createEntry(self, data):

        # Format:
        # data = {
        #    "FileID": "xxx",
        #    "Division": "xxx",
        #    "FileName": "xxx",
        #    "Cycle": "xxx",
        #    "OldData": "xxx",
        #    "Tag1": "xxx"
        # }
        try:
            entry = await self.db.file.create(data=data)
            return entry
        except Exception as e:
            print("CREATE FAILED, SKIPPING\n")
            print(e)
            return None

    async def update_file(self, file_id, data):

        # data is a dictionary that can contain any of the created fields to be 
        # updated, excluding FileID.

        # data = {
        #   "Division": "yyy",
        # }

        entry = await self.db.file.update(where={"FileID": file_id}, data=data)
        return entry

    async def delete_file(self, file_id):
        await self.db.file.delete(where={"FileID": file_id})
        return

    async def clear_database(self):
        await self.db.file.delete_many()
        return

    async def search(self, data, order='asc'):
        # returns all entries that match the provided data param

        # default order is ascending, can be changed to descending by providing
        # the order param as "desc"

        # data = {
        #  "Division": "yyy",
        #  "Cycle": "xxx",
        # }

        # search() with the above data returns all entries where Division is
        # "yyy" and Cycle is "xxx"

        entries = await self.db.file.find_many(where=data, order=order)
        return entries