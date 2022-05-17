Run:
-flask run

Create Database:
-flask shell
-from src.database import db
-db.create_all() //creation
-db.drop_all()  //delete


API Request:
http://127.0.0.1:5000/api/v1/batteries/get_values?user=1