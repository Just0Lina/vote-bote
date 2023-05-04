import dal.request
import dal.tables
import dal.database

# Database data
DB = database.Database()
if DB.isConnected():
    print("Seems good")
else:
    print("Database initialization failed")

