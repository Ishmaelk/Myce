import googlemaps
import pandas as pd
#gmaps_key = googlemaps.Client(key = "AIzaSyCaSefpc8ANF32twj7-CNbd0p2u2KdQV2M")
df = pd.read_csv("NYC Restaurants Geocoded - Sheet1.csv", delimiter = ',',
	 names = ['name', 'LAT', 'LON', 'LATLON'])
df['address'] = None
for row in df['name']:
	
	for i in range(0, len(row)):
		if row[i].isdigit(): # split the string by index, palce in df['name'] palce address in df['address']
			df['name'][i] = row[0:i-1]
			df['address'][i] = row[i:]
			print (df['name'][i] + " | " + df['address'][i])
			break
		
''' GOOGLE GEOCODING SHIT
for i in range(0, len(df), 1):
	geocode_result = gmaps_key.geocode(df.iat[i, 0])
	print ("here");
	try:
		lat = geocode_result[0]["geometry"]["location"]["lat"]
		lon = geocode_result[0]["geometry"]["location"]["lng"]
		df.iat[i, df.columns.get_loc("LAT")] = lat
		df.iat[i, df.columns.get_loc("LON")] = lon
		print (lat + " " + lon)
	except:
		lat = None
		lon = None
'''
