import mysql.connector
import json
from copy import deepcopy

myce_db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="password",
    database="Myce"
)

print(myce_db)

cursor = myce_db.cursor()

# SHOWTABLES = "SHOW TABLES"
# SHOW_DATABASES = "SHOW DATABASES"
# attributes = []

# FIRST DO THIS:

# --------------------------UPLOADING RAW DATA (COPY)------------------------------
# cursor.execute("SHOW DATABASES")
#cursor.close()

# cursor = myce_db.cursor()


# get_all = "SELECT * FROM file_data"
# cursor.execute("SET_SESSION sql_mode = '' ")
#cursor.execute("SELECT * FROM file_data WHERE DBA = 'DJ REYNOLDS PUB AND RESTAURANT' ")
# cursor.execute("SELECT * FROM file_data ORDER BY CAMIS")
# cursor.execute("SELECT * FROM violations")
# results = cursor.fetchall()
# cursor.execute("SELECT * FROM file_data WHERE DBA = 'DJ REYNOLDS PUB AND RESTAURANT' ")
# results2 = cursor.fetchall()
#
# for entry in results:
#     print(entry)
# for entry in results2:
#     print(entry)




# # cursor.execute("DROP TABLE IF EXISTS file_data");
# #
# # data = "CREATE TABLE file_data( CAMIS VARCHAR(8), DBA VARCHAR(150), BORO VARCHAR(15),"
# #        "BUILDING VARCHAR (20), STREET VARCHAR(80), ZIPCODE VARCHAR(6),PHONE VARCHAR(20),"
# #         "CUISINE_DESCRIPTION VARCHAR(200), INSPECTION_DATE VARCHAR(10), ACTION_ VARCHAR(200),"
# #         "VIOLATION_CODE VARCHAR(3), SCORE VARCHAR(15), GRADE VARCHAR(15), GRADE_DATE VARCHAR(10),"
# #         "INSPECTION_TYPE VARCHAR(100) )"
# #
# # cursor.execute(data);
#
# for db in cursor:
#     print(db)
#
# print("\n")
#
# print("I'M HERE")
#
# file = open("nyc_open_data.json", "r")
#
# the_file = file.read()
#
# working_data = json.loads(the_file)
#
# print( type(working_data) )
# print("\n")
# #
# # for key in working_data["meta"]["view"]["columns"]:
# #     if(key["id"] > -1):
# #         print(key["name"] + "\t\t\t\t" + key["dataTypeName"])
# #         attributes.append(key["name"])
#
# # print("\n")
# # for key in working_data:
# #     print(key)
# # print("I'M HERE NOW")
#
# print("\n")
# #
# # for attribute in attributes:
# #     print(attribute)
#
# del working_data["meta"]
#
# #deleting the first 8 useless data
# for data in working_data["data"]:
#         del data[:8]
#
# #adjusting the data's so it has 10 characters
# for data in working_data["data"]:
#     if(data[8] != None):
#         data[8] = data[8][:10]
#     if(data[15] != None):
#         data[15] = data[15][:10]
#     if(data[16] != None):
#         data[16] = data[16][:10]
#
# # for data in working_data["data"]:
# #      print(data)
#
# for data in working_data["data"]:
#     tupledata1 = tuple(data)
#     cursor.execute("INSERT INTO file_data (CAMIS, DBA, BORO, BUILDING, STREET, ZIPCODE, PHONE, "
#                    "CUISINE_DESCRIPTION, INSPECTION_DATE, ACTION_, VIOLATION_CODE, VIOLATION_DESCRIPTION,"
#                    "CRITICAL_FLAG, SCORE, GRADE, GRADE_DATE, RECORD_DATE, INSPECTION_TYPE) VALUES(%s, %s, %s, %s, %s,"
#                    "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", tupledata1)
#
# myce_db.commit()
#------------------------------UPLOADING RAW DATA (COPY)----------------------------

#NEXT DO THIS:


# # -----------------------UPLOADING DATA (VIOLATIONS)----------------------------
#
# # name_of_business = "'DUNKIN DONUTS'"
# # get_business = "SELECT * FROM file_data WHERE DBA = " + name_of_business


# def callvio(thecursor):
#
#     cursor.execute("SELECT * FROM violations")
#     vioresults = cursor.fetchall()
#     for entry in vioresults:
#         print(entry)
#
#     print("The top one worked!")
#     thecursor.execute("SELECT * FROM violations")
#     vioresults = thecursor.fetchall()
#     for entry in vioresults:
#         print(entry)
#
#     return;
#
# callvio(cursor)


get_order = "SELECT * FROM cond_file_data ORDER BY CAMIS, INSPECTION_DATE"
#
# map_of_vio = {}
#
cursor.execute(get_order)
# #
# # # sql_command = "SELECT * FROM file_data WHERE DBA = 'DUNKIN DONUTS' "
# #
results = cursor.fetchall()
# #
# # print(results[0])
# # print("\n")
# # print(results[1])

start = tuple(list(results[0]))
stop = None;
date_to_watch = results[0][8]
id_to_watch = results[0][0]
copyresults = tuple(list(results))

i = 1

def condense(start, stop, copyresults):
    counter = 0
    violation_array = []
    flag = 0
    for row in copyresults:
        if(row == stop):
            if(counter > 1):
                print("I was here")
                cursor.execute("DELETE FROM cond_file_data WHERE (CAMIS, INSPECTION_DATE, VIOLATION_CODE) VALUES (%s,"
                               "%s, %s)", [str(start[0]), str(start[8]), start[10]], " LIMIT " + str(counter - 1))
                print("Now i'm here")
                string_vio = ""
                for code in violation_array:
                    if(code != violation_array[len(violation_array) - 1]):
                        string_vio = string_vio + code + ' '
                    else:
                        string_vio = string_vio + code

                print(string_vio)


                cursor.execute("UPDATE cond_file_data SET (VIOLATION_CODE) WHERE (CAMIS, INSPECTION_DATE) VALUES (%s,"
                               " %s, %s)", [string_vio, str(start[0]), str(start[8])])

                # cursor.execute("UPDATE cond_file_data SET VIOLATION_CODE = " + string_vio + " WHERE CAMIS = " +
                #                str(start[0]) + " AND INSPECTION_DATE = " + str(start[8]))
        elif(start == row):
            violation_array.append(row[10])
            counter = counter + 1
            flag = 1
        elif(flag == 1):
            violation_array.append(row[10])
            counter = counter + 1
    return;


for i in range(len(results)):
    if((date_to_watch != results[i][8]) or (id_to_watch != results[i][0])):
        stop = tuple(list(results[i]))
        condense(start, stop, copyresults)
        start = tuple(list(results[i]))
        date_to_watch = results[i][8]
        id_to_watch = results[i][0]

myce_db.commit()

print("WE DONE BOYS")


# #
# # for row in results:
# #     if(map_of_vio.get(row[11], "XXX") == "XXX"):
# #         map_of_vio.update({row[10]: [row[11], row[12]]})
# # # #
# # for violation, desc in map_of_vio.items():
# #         print(violation, desc)
# #         entry = (violation, desc[0], desc[1])
# #         cursor.execute("INSERT INTO violations(VIOLATION_CODE, VIOLATION_DESCRIPTION, "
# #                        "CRITICAL_FLAG) VALUES (%s, %s, %s)", entry)
# # myce_db.commit()
#
# # ------------------------UPLOADING DATA (VIOLATIONS)------------------


#NOW DROP THE FIRST file_data, then run this:


# # --------------------------UPLOADING SHORTENED DATA To database------------------------------
# cursor.execute(SHOWDATABASES)
#
# for db in cursor:
#     print(db)
#
#
# file = open("nyc_open_data.json", "r")
#
# the_file = file.read()
#
# working_data = json.loads(the_file)
#
# print( type(working_data) )
# print("\n")
#
# print("\n")
#
# del working_data["meta"]
#
# # deleting the first 8 useless data
# for data in working_data["data"]:
#         del data[:8]
#
# # adjusting the data's so it has 10 characters
# for data in working_data["data"]:
#     if(data[8] != None):
#         data[8] = data[8][:10]
#     if(data[15] != None):
#         data[15] = data[15][:10]
#     if(data[16] != None):
#         data[16] = data[16][:10]
#     # print(data[11])
#     del data[11]
#     # print(data[11])
#     del data[11]
#     # print(data[14])
#     del(data[14])
#
#
# # for data in working_data["data"]:
# #      print(data)
#
# for data in working_data["data"]:
#     tupledata1 = tuple(data)
#     cursor.execute("INSERT INTO file_data (CAMIS, DBA, BORO, BUILDING, STREET, ZIPCODE, PHONE, "
#                    "CUISINE_DESCRIPTION, INSPECTION_DATE, ACTION_, VIOLATION_CODE, SCORE, "
#                    "GRADE, GRADE_DATE, INSPECTION_TYPE) VALUES (%s, %s, %s, %s, %s,"
#                    "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", tupledata1)
# myce_db.commit()
# # ------------------------------UPLOADING SHORTENED DATA----------------------------







print("\n")
print("Now I'm selecting data")




print("DONE!")




# -------TRYING TO DO PSEUDO CODE-------------



#
# So I can remove the:
#
# -violation description
# -the critical flag
# -record date
#
# from the main DB
#
# -condense all the violation codes to one day per inspection times

# temp_array = []
# gradedate = null
# for entry in ordered_results:
#     if(len(temp_array) == 0){
#         temp_array =
#     }
#     else{
#           if(entry[gradedate] > date):
#                 temp_array.clear()
#                 date = entry[gradedate]
#                 temp_array.push(entry[violationcode])
#     }
#     while(entry[0])

# # 1)make a map like so: [CAMIS]: [ [VIOLATIONS], DATEGRADED]
# # 2)update the table once per unqiue date and CAMIS
#
# can do like this
# if(entry[camis] == map.get(camis) && entry[date] == map.get(camis))
# # 3)delete if seen once in table









# start from one, store the violationcode, date, camis into a temps
# (array for violationcodearray, temp variable for violationcode if match)
#
# 1) FIRST RUN
# if next CAMIS == tempCAMIS && DATE == tempDATE{
#     store violation code into a temp variable
#     update entry by adding in the stored violationcodearray
#     push temp variable into violationcodearray
#
# else{
#     clear violationcodearray
#     push new violation code into violationcodearray
#     store date and camis into temps
# }
#
# 2)SECOND Run
# //peek by 1?

# --------------------------HACKATHONG ---------------------------
# temp = [1, 2, 3, 4, 5]
#
# for i in range(len(temp)):
#     print("output number: " + str(temp[i]))
#     if(temp[i + 1] == 2):
#         print("HERE" + str(temp[i + 1]))
#         del temp[i + 1]
#
# Start = results[0].slice()
# Stop = null
# #Data_to_cond = [ ]
# #Data_to_cond.append(results[0])
# Date_to_watch = results[0][dateindex]
# Id_to_watch = results[0][CAMISindex]
# Copyresults = results.slice()
#
# i = 1 #so we start with the next index since we preloaded everything
#
# For i in range(len(results)):
#
# //if( id != id_to_watch)
#        Call condesne
#     Else if(date != date_to_watch)
#
#    If(results[i][dateindex] != date_to_watch  && results[i][CAMISindex] != id_to_watch):
#           Stop = results[i].slice()
#           Condense(Start, Stop, copyresults)
#           Start = results[i].slice()
#           Date_to_watch = results[i][dateindex]
#    Else:
#
#
#
#
# Function Condense(start, stop, copyresults):
#      -search for start
#      -once found, enter a loop that keeps going until you got start
#            -in the loop, you drag the violation code into the next entry, and you increment a counter by 1
#            -once you hit stop, you break the loop
#
#
#      -now you find start again, and this is where the counter comes into play.
#      -you delete the first entry, and decrement counter by 1.
#     You keep doing this for each successive entry until you get the counter of....1, once you hit 1,
#     you have reached the entry you need to keep, then you break. And boom, you done condensing and deleting





# # # map_of_vio = {}
# # #
# cursor.execute(get_order)
# #
# # # sql_command = "SELECT * FROM file_data WHERE DBA = 'DUNKIN DONUTS' "
# #
# results = cursor.fetchall()
# #
# # print(results[0])
# # print("\n")
# # print(results[1])
# for entry in results:
#       print(entry)
# #
# # for row in results:
# #     if(map_of_vio.get(row[11], "XXX") == "XXX"):
# #         map_of_vio.update({row[10]: [row[11], row[12]]})



# --------------------COPYING ISH'S DATA--------------------
'''
temp_array = [2, 4, 6]
temp_array2 = [1, 3, 5]
temp_array3 = [temp_array2[0], temp_array2[2]]
new_tuple = tuple(temp_array + temp_array3)

print(new_tuple)


rows = []

cursor.execute("SET SESSION sql_mode =' '")

with open('NYC Restaurants Geocoded - Sheet1.csv') as f:
    for line in f:
        components = line.split(',')
        row = components[0]
        for i in range(0, len(row)):
            if row[i].isdigit(): # split the string by index
                name = row[0:i-1]
                address = row[i:]
                components[0] = name
                components.append(address)
                break
        rows.append(components)
        #print (components)
print ('here')

insert_formula = "INSERT INTO geocoding (business_name, address, lat, lon) VALUES (%s, %s, %s, %s)"

print ("Populating")
# POPULATING CODE CODE

for row in rows:
    insertion = (row[0], row[len(row)-1], row[1], row[2])
    print(insertion)
    cursor.execute(insert_formula, insertion)

# AFTER COMPLETION
myce_db.commit()
'''
# --------------------COPYING ISH'S DATA END--------------------

# map_of_saif = {}
# 
# cursor.execute("SELECT * FROM geocoding")
# ish_data = cursor.fetchall()
# # cursor.execute("SELECT * FROM file_data WHERE BUILDING IS NOT NULL AND STREET IS NOT NULL AND ZIPCODE IS NOT NULL "
# #                "ORDER BY CAMIS")
# 
# cursor.execute("SELECT * FROM file_data WHERE BUILDING IS NOT NULL AND STREET IS NOT NULL AND ZIPCODE IS NOT NULL "
#                "AND (ZIPCODE = 10314) ORDER BY CAMIS")
# 
# #ZIPCODE =
# 
# 
# saif_data = cursor.fetchall()

for data in saif_data:
    temp_thing = (None, None)
    tupledata1 = tuple(data + temp_thing)
    cursor.execute("INSERT INTO final_file_data (CAMIS, DBA, BORO, BUILDING, STREET, ZIPCODE, PHONE, "
                   "CUISINE_DESCRIPTION, INSPECTION_DATE, ACTION_, VIOLATION_CODE, SCORE, "
                   "GRADE, GRADE_DATE, INSPECTION_TYPE, lat, lon) VALUES (%s, %s, %s, %s, %s,"
                   "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", tupledata1)

# myce_db.commit()
# print("I done with population FINAL_FILE_DATA")
# 
# 
#creating map of saif
for saif_row in saif_data:
    saif_address = saif_row[3] + " " + saif_row[4] + " New York NY" + " " + saif_row[5]
    if (map_of_saif.get(saif_address, "XXX") == "XXX"):
        map_of_saif.update({saif_address: saif_row})
# 
# 
# print("WE DONE WITH FILLING ME UP")
# 
for ish_row in ish_data:
    if(map_of_saif.get(ish_row[1], "XXX") != "XXX"):
        matching_camis = map_of_saif[ish_row[1]][0]
        latt = str(ish_row[2])
        long = str(ish_row[3])
        cursor.execute("UPDATE final_file_data SET lat = " + latt + ", lon = " + long + "WHERE CAMIS = " +
                       matching_camis)
# 
# myce_db.commit()
# 
# print("WE MADE IT")



#
# for row in results:
#     if(map_of_vio.get(row[11], "XXX") == "XXX"):
#         map_of_vio.update({row[10]: [row[11], row[12]]})


# For ish_row in ISHS:
#     For saif_row in SAIFS:
#         saif_address = saif_row[3] + “ “  + saif_row[4] + “ New York NY” + “ “ + saif_row[5]
#         if(saif_address == ish_row[1]):
#             temp_array = [ish_row[2], ish_row[3]]
#             new_entry = tuple(saif_row + temp_array)
#             cursor.execute("INSERT INTO final_file_data (CAMIS, DBA, BORO, BUILDING, STREET, ZIPCODE, PHONE, "
#                    "CUISINE_DESCRIPTION, INSPECTION_DATE, ACTION_, VIOLATION_CODE, SCORE, "
#                    "GRADE, GRADE_DATE, INSPECTION_TYPE, lat, lon) VALUES (%s, %s, %s, %s, %s,"
#                    "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s , %s, %s)", new_entry)


'''
UPDATE Customers
SET ContactName = 'Alfred Schmidt', City= 'Frankfurt'
WHERE CustomerID = 1;
'''




#Question is, can I make a tuple out of (saif_row + ish_row[3] + ish_row[4])


# here 8:48pm
# #CODING FOR MERGING BELOW---------------------------------------------------------------------
# 37 WEST 65 STREET New York NY 10023
#
#
# BUIDLING + STREET + “New York NY” +  ZIPCODE
#






#
# For ish_row in ISHS:
#     For saif_row in SAIFS:
#         saif_address = saif_row[3] + “ “  + saif_row[4] + “ New York NY” + “ “ + saif_row[5]
#         if(saif_address == ish_row[1]):
#             temp_array = [ish_row[2], ish_row[3]]
#             new_entry = tuple(saif_row + temp_array)
#             cursor.execute("INSERT INTO final_file_data (CAMIS, DBA, BORO, BUILDING, STREET, ZIPCODE, PHONE, "
#                    "CUISINE_DESCRIPTION, INSPECTION_DATE, ACTION_, VIOLATION_CODE, SCORE, "
#                    "GRADE, GRADE_DATE, INSPECTION_TYPE, lat, lon) VALUES (%s, %s, %s, %s, %s,"
#                    "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s , %s, %s)", new_entry)
#
#
#
# for data in working_data["data"]:
#     tupledata1 = tuple(data)
#     cursor.execute("INSERT INTO file_data (CAMIS, DBA, BORO, BUILDING, STREET, ZIPCODE, PHONE, "
#                    "CUISINE_DESCRIPTION, INSPECTION_DATE, ACTION_, VIOLATION_CODE, SCORE, "
#                    "GRADE, GRADE_DATE, INSPECTION_TYPE) VALUES (%s, %s, %s, %s, %s,"
#                    "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", tupledata1)
# myce_db.commit()
# #
# #
# #
# #
# # lat DECIMAL(13, 10), lon DECIMAL(13, 10)
#
#
# cursor.execute("SELECT * FROM geocoding")
# ishs_Data = cursor.fetchall()'
#
# for row in ishs_Data:
#     row[1] ==

#Manhattan

#central harlem
#chelse and clinton
#east harlem
#Gramercy Park and Murray Hill
#Greenwich Village and Soho
#Lower Manhattan
#LOWER EAST SIDE
#UPPER EAST SIDE
#UPPER WEST SIDE
#Inwood and Washington Heights

#Brooklyn

#Central Brooklyn
#Southwest Brooklyn
#Borough Park
#Canarsie and Flatlands
#Southern Brooklyn
#Northwest Brooklyn
#Flatbush
#East New York and New Lots
#Greenpoint
#Sunset Park
#Bushwick and Williamsburg

#Queens
'''
Northeast Queens 

North Queens 

Central Queens 

Jamaica 

Northwest Queens

West Central Queens 

Rockaways

Southeast Queens 

Southwest Queens

West Queens 
'''



#Bronx
'''
Southeast Bronx 

Central Bronx

Bronx Park and Fordham 

High Bridge and Morrisania 

Hunts Point and Mott Haven 

Kingsbridge and Riverdale 

Northeast Bronx 
'''

#staten_island
'''
Port Richmond 

South Shore

Stapleton and St. George 

Mid-Island
'''


#-----------------------------ALGORITHM TO CONDENSE DATA BELOW-----------------------------
#
# # name_of_business = "'DUNKIN DONUTS'"
# # get_business = "SELECT * FROM file_data WHERE DBA = " + name_of_business


# def callvio(thecursor):
#
#     cursor.execute("SELECT * FROM violations")
#     vioresults = cursor.fetchall()
#     for entry in vioresults:
#         print(entry)
#
#     print("The top one worked!")
#     thecursor.execute("SELECT * FROM violations")
#     vioresults = thecursor.fetchall()
#     for entry in vioresults:
#         print(entry)
#
#     return;
#
# callvio(cursor)


get_order = "SELECT * FROM cond_file_data ORDER BY CAMIS, INSPECTION_DATE"
#
# map_of_vio = {}
#
cursor.execute(get_order)
# #
# # # sql_command = "SELECT * FROM file_data WHERE DBA = 'DUNKIN DONUTS' "
# #
results = cursor.fetchall()
# #
# # print(results[0])
# # print("\n")
# # print(results[1])

start = tuple(list(results[0]))
stop = None;
date_to_watch = results[0][8]
id_to_watch = results[0][0]
copyresults = tuple(list(results))

i = 1

def condense(start, stop, copyresults):
    counter = 0
    violation_array = []
    flag = 0
    for row in copyresults:
        if(row == stop):
            if(counter > 1):
                print("I was here")
                cursor.execute("DELETE FROM cond_file_data WHERE (CAMIS, INSPECTION_DATE, VIOLATION_CODE) VALUES (%s,"
                               "%s, %s)", [str(start[0]), str(start[8]), start[10]], " LIMIT " + str(counter - 1))
                print("Now i'm here")
                string_vio = ""
                for code in violation_array:
                    if(code != violation_array[len(violation_array) - 1]):
                        string_vio = string_vio + code + ' '
                    else:
                        string_vio = string_vio + code

                print(string_vio)


                cursor.execute("UPDATE cond_file_data SET (VIOLATION_CODE) WHERE (CAMIS, INSPECTION_DATE) VALUES (%s,"
                               " %s, %s)", [string_vio, str(start[0]), str(start[8])])

                # cursor.execute("UPDATE cond_file_data SET VIOLATION_CODE = " + string_vio + " WHERE CAMIS = " +
                #                str(start[0]) + " AND INSPECTION_DATE = " + str(start[8]))
        elif(start == row):
            violation_array.append(row[10])
            counter = counter + 1
            flag = 1
        elif(flag == 1):
            violation_array.append(row[10])
            counter = counter + 1
    return;


for i in range(len(results)):
    if((date_to_watch != results[i][8]) or (id_to_watch != results[i][0])):
        stop = tuple(list(results[i]))
        condense(start, stop, copyresults)
        start = tuple(list(results[i]))
        date_to_watch = results[i][8]
        id_to_watch = results[i][0]

myce_db.commit()

print("WE DONE BOYS")