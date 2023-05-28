import gridfs
from pymongo import MongoClient
import base64
import gridfs
import globalvar
import os


class Config:
    def __init__(self):
        self.connection_str = 'mongodb+srv://devoza:12345@x-ray-cluster.wlwm3cu.mongodb.net/?retryWrites=true&w=majority'
        self.client = MongoClient(self.connection_str)

    def create_collection(self, collection_name):
        db = self.client['CPN']
        collection = db[collection_name]
        return collection

    def insert_data(self, collection_name, data):
        collection = self.create_collection(collection_name)
        collection.insert_one(data)

    def get_Data_By_Specific_Field(self, collection_name, fieldName, value):
        db = self.client['CPN']
        collection = db[collection_name]
        query = {}
        query[fieldName] = value
        result = list(collection.find(query))
        return result

    def get_Data_By_Fields(self, collection_name, fieldNames, values):
        db = self.client['CPN']
        collection = db[collection_name]

        query = {}
        for i in range(0, len(fieldNames)):
            query[fieldNames[i]] = values[i]

        result = list(collection.find(query))
        return result

    def uploadPDF(self, path):
        db = self.client['CPN']
        fs = gridfs.GridFS(db)
        # Note, open with the "rb" flag for "read bytes"

        with open(path, "rb") as f:
            encoded_string = base64.b64encode(f.read())
        with fs.new_file(
                chunkSize=800000,
                filename=path,
                email=globalvar.email) as fp:
            fp.write(encoded_string)
        os.remove(path)
        # print("File uploaded successfully")

    def fetch_pdf(self):

        db = self.client['CPN']
        fs = gridfs.GridFS(db)

        for pdf in db.fs.files.find({'email': globalvar.email}):
            globalvar.uploaded_files.append(
                {"filename": pdf['filename'], "date": pdf['uploadDate']})

    def read_pdf(self, filename):
        db = self.client['CPN']
        fs = gridfs.GridFS(db)

        data = fs.find_one(filter=dict(filename=filename))
        with open("C:/Users/devoz/Downloads/" + filename, "wb") as f:
            f.write(base64.b64decode(data.read()))
        # print("File downloaded successfully")
