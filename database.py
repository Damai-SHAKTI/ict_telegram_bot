from pymongo import MongoClient


def get_database():
    CONNECTION_STRING = "mongodb+srv://admin:wEYxUlM9h7g4wAuT@cluster0.t0nvdt0.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(CONNECTION_STRING)
    return client['telegram']


if __name__ == "__main__":
    # Get the database
    dbname = get_database()
