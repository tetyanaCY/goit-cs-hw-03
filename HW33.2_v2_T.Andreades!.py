from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure, PyMongoError
from faker import Faker
import random

# Initialize Faker with Ukrainian localization
fake = Faker("uk_UA")
Faker.seed(0)
random.seed(0)

def generate_features():
    # Generates a random list of features for cats
    features = [
        "дає себе гладити", "рудий", "любить спати на сонці",
        "мурчить, коли щасливий", "полює за лазером",
        "не любить купатися", "завжди голодний", "має унікальні вуса",
        "дружелюбний до гостей"
    ]
    return random.sample(features, 3)

def connect_to_db():
    try:
        # Attempt to establish a connection to MongoDB
        client = MongoClient("mongodb+srv://***:***@cluster0.ihkjani.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
        db = client["test"]
        collection = db["cats"]
        print("Connected to MongoDB.")
        return collection
    except ConnectionFailure:
        print("MongoDB database connection error.")
        return None

def create_cat(collection, cat):
    # Function to create a new cat entry in the database
    try:
        collection.insert_one(cat)
        print(f"Cat {cat.get('name')} was created.")
    except PyMongoError as e:
        print(f"Error when creating new cat in the database: {e}")

def read_all(collection):
    # Reads and displays all cats from the collection
    try:
        cats = collection.find()
        for cat in cats:
            print(cat)
    except PyMongoError as e:
        print(f"Error retrieving cats: {e}")

def read_by_name(collection, name):
    # Reads and displays a cat by name from the collection
    try:
        cat = collection.find_one({"name": name})
        if cat:
            print(cat)
        else:
            print(f"Cat with name {name} not found.")
    except PyMongoError as e:
        print(f"Error finding cat by name: {e}")

def update_cat_age_by_name(collection, name, new_age):
    # Updates the age of a cat by name
    try:
        result = collection.update_one({"name": name}, {"$set": {"age": new_age}})
        if result.modified_count:
            print(f"Cat {name}'s age updated to {new_age}.")
        else:
            print(f"Cat {name} not found.")
    except PyMongoError as e:
        print(f"Error updating cat's age: {e}")

def add_feature_to_cat_by_name(collection, name, new_feature):
    # Adds a new feature to a cat by name
    try:
        result = collection.update_one({"name": name}, {"$push": {"features": new_feature}})
        if result.modified_count:
            print(f"Feature '{new_feature}' added to cat {name}.")
        else:
            print(f"Cat {name} not found for feature addition.")
    except PyMongoError as e:
        print(f"Error adding feature to cat: {e}")

def delete_cat_by_name(collection, name):
    # Deletes a cat by name from the collection
    try:
        result = collection.delete_one({"name": name})
        if result.deleted_count:
            print("Запис видалено.")
        else:
            print("Запису з таким іменем не знайдено.")
    except PyMongoError as e:
        print(f"Error during cat deletion by name: {e}")

def delete_all(collection):
    # Deletes all records from the collection
    try:
        collection.delete_many({})
        print("All records deleted.")
    except PyMongoError as e:
        print(f"Error during the deletion of all records: {e}")

if __name__ == '__main__':
    collection = connect_to_db()
    if collection is not None:
        cat = {"name": "barsik", "age": 3, "features": ["playful", "friendly"]}
        create_cat(collection, cat)
        read_all(collection)
        read_by_name(collection, "barsik")
        update_cat_age_by_name(collection, "barsik", 4)
        add_feature_to_cat_by_name(collection, "barsik", "спить день напроліт")
        read_by_name(collection, "barsik")  # To verify updates
        delete_cat_by_name(collection, "barsik")
        delete_all(collection)  # Use with caution; this will remove all cats!
