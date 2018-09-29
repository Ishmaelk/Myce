import mysql.connector
import json

myce_db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "password",
    database = "Myce"
)

cursor = myce_db.cursor()


SHOWTABLES = "SHOW TABLES"
SHOWDATABASES = "SHOW DATABASES"
attributes = []

#FIRST DO THIS:

#--------------------------UPLOADING RAW DATA (COPY)------------------------------
cursor.execute(SHOWDATABASES)

cursor.execute("DROP TABLE IF EXISTS file_data");
data = "CREATE TABLE file_data( CAMIS VARCHAR(8), DBA VARCHAR(150), BORO VARCHAR(15),"
       "BUILDING VARCHAR (20), STREET VARCHAR(80), ZIPCODE VARCHAR(6),PHONE VARCHAR(20),"
        "CUISINE_DESCRIPTION VARCHAR(200), INSPECTION_DATE	VARCHAR(10), ACTION_ VARCHAR(200),"
        "VIOLATION_CODE VARCHAR(3), SCORE VARCHAR(15), GRADE VARCHAR(15), GRADE_DATE VARCHAR(10),"
        "INSPECTION_TYPE VARCHAR(100) )"

cursor.execute(data);

for db in cursor:
    print(db)

print("\n")

print("I'M HERE")

file = open("nyc_open_data.json", "r")

the_file = file.read()

working_data = json.loads(the_file)

print( type(working_data) )
print("\n")
#
# for key in working_data["meta"]["view"]["columns"]:
#     if(key["id"] > -1):
#         print(key["name"] + "\t\t\t\t" + key["dataTypeName"])
#         attributes.append(key["name"])

# print("\n")
# for key in working_data:
#     print(key)
# print("I'M HERE NOW")

print("\n")
#
# for attribute in attributes:
#     print(attribute)

del working_data["meta"]

#deleting the first 8 useless data
for data in working_data["data"]:
        del data[:8]

#adjusting the data's so it has 10 characters
for data in working_data["data"]:
    if(data[8] != None):
        data[8] = data[8][:10]
    if(data[15] != None):
        data[15] = data[15][:10]
    if(data[16] != None):
        data[16] = data[16][:10]

# for data in working_data["data"]:
#      print(data)

for data in working_data["data"]:
    tupledata1 = tuple(data)
    cursor.execute("INSERT INTO file_data (CAMIS, DBA, BORO, BUILDING, STREET, ZIPCODE, PHONE, "
                   "CUISINE_DESCRIPTION, INSPECTION_DATE, ACTION_, VIOLATION_CODE, VIOLATION_DESCRIPTION,"
                   "CRITICAL_FLAG, SCORE, GRADE, GRADE_DATE, RECORD_DATE, INSPECTION_TYPE) VALUES(%s, %s, %s, %s, %s,"
                   "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", tupledata1)

myce_db.commit()
#------------------------------UPLOADING RAW DATA (COPY)----------------------------

#NEXT DO THIS:


# # -----------------------UPLOADING DATA (VIOLATIONS)----------------------------
#
# # name_of_business = "'DUNKIN DONUTS'"
# # get_business = "SELECT * FROM file_data WHERE DBA = " + name_of_business
# get_order = "SELECT * FROM file_data ORDER BY CAMIS, INSPECTION_DATE"
# # # # #
# # # map_of_vio = {}
# # #
# cursor.execute(get_order)
# #
# # # sql_command = "SELECT * FROM file_data WHERE DBA = 'DUNKIN DONUTS' "
# #
# results = cursor.fetchall()]
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



































