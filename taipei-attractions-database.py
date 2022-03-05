import requests, json, mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    port="3306",
    user="root",
    password="12345678",
    database="travelDB"
)
mycursor = mydb.cursor()

url = 'https://raw.githubusercontent.com/klina916/Origin-Repository/main/data/taipei-attractions.json'
resp = requests.get(url)
resp.encoding = 'utf-8'

data = json.loads(resp.text)

results = data["result"]["results"]

sql = "INSERT INTO taipeiAttractions (id,name,category,description,address,transport,mrt,latitude,longitude,images) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

for n in results:
    if n["_id"]:
        list=(n["_id"],n["stitle"],n["CAT1"],n["xbody"],n["address"],n["info"],n["MRT"],n["latitude"],n["longitude"],n["file"])
        mycursor.execute(sql, list)
mydb.commit()

sql2 ="INSERT INTO taipeiAttractionsImages (imageId, imageUrl) values (%s, %s)"

for j in results:
    for k in range(1,len(j["file"].split("http"))):
        pic_url="http"+j["file"].split("http")[k]
        list=(j["_id"],pic_url)
        mycursor.execute(sql2, list) 
mydb.commit()

mycursor.close()
mydb.close()