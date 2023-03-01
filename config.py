from pymongo import MongoClient

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
        