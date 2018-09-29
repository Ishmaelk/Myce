import json
import mysql.connector

mydb = mysql.connector.connect (
	host = "localhost",
	user = "root",
	passwd= 'i18111958',
	database= "myce_yelp"
)

mycursor = mydb.cursor()

mycursor.execute("DROP TABLE IF EXISTS restaurants")

mydb.commit()

mycursor.execute("CREATE TABLE restaurants (business_id VARCHAR(255), name VARCHAR(255), address VARCHAR(255), city VARCHAR(255), state VARCHAR(255), postal_code VARCHAR(255), latitude DECIMAL(13, 10), longitude DECIMAL(13, 10), stars DECIMAL(2, 1), review_count INTEGER(10))");

insertion_formula = "INSERT INTO restaurants (business_id, name,address, city, state, postal_code, latitude, longitude,stars, review_count) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

test_insertion = ("666", "Devil's ass drills", "666 Hell Street", "Hell City", "Hell", "66666", 666, 666, 0, 666)

mycursor.execute(insertion_formula, test_insertion)

mydb.commit()

