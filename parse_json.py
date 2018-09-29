from builtins import any
import mysql.connector
ny_restaurants = []

# Populate database with array of dictionaries #
mydb = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        passwd = 'i18111958',
        database = 'myce_yelp'
)

mycursor = mydb.cursor()

mycursor.execute("DROP TABLE IF EXISTS restaurants")
mycursor.execute("SET SESSION sql_mode = ''")
mydb.commit()

mycursor.execute("CREATE TABLE restaurants (business_id VARCHAR(255) NULL, name VARCHAR(255) NULL, address VARCHAR(255) NULL, city VARCHAR(255) NULL, state VARCHAR(255) NULL, postal_code VARCHAR(255) NULL, latitude DECIMAL(13, 10) NULL, longitude DECIMAL(13, 10) NULL, stars DECIMAL(2, 1) NULL, review_count INTEGER(10) NULL)");

keys = ["business_id", "name", "address", "city", "state", "postal_code", "latitude", "longitude", "stars", "review_count"]

tup = (keys[0], keys[1], keys[2], keys[3], keys[4], keys[5], keys[6], keys[7], keys[8], keys[9])
print (tup)

with open ('yelp_academic_dataset_business.json') as f:
	for line in f:
		line = line.lower();
		line = line.replace("\"", "")
		# if not a restaurant or is closed or not in NY
		#if "restaurant" not in line or "is_open:0" in line or "state:ny" not in line:
		#	continue
		line = line[1:]
		line = line[:-1]
		info_map = {}
		while (line != ""):
			if line[0] == ',':
				line = line[1:]
			info_split = line[: line.find(',')]
			key_value = info_split.split(':')
			if len(key_value) > 1:	
				key = key_value[0];
				needed = any(key in x for x in keys)
				if needed:
					info_map[key] = key_value[1];
					#print ("KEY: " + key + " VALUE: " + info_map[key]) 
			line = line[len(info_split)+1:]
		if info_map: # if it has been populated
			ny_restaurants.append(info_map)

# Populate database with array of dictionaries #

insertion_formula = "INSERT INTO restaurants (business_id, name, address, city, state, postal_code, latitude, longitude,stars, review_count) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

for d in ny_restaurants:
	row = (d[keys[0]], d[keys[1]], d[keys[2]], d[keys[3]], d[keys[4]], d[keys[5]], d[keys[6]], d[keys[7]], d[keys[8]], d[keys[9]])
	mycursor.execute(insertion_formula, row)
mydb.commit()
	





