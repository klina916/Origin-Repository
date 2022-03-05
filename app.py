from flask import *
import re

app=Flask(__name__)
app.secret_key="eiddccidtcdbjlgennuivccuehhdeubkb"
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True

import mysql.connector
mydb = mysql.connector.connect(
    host="localhost",
    port="3306",
    user="root",
    password="12345678",
    database="travelDB"
)
mycursor = mydb.cursor()

# Pages
@app.route("/")
def index():
	return render_template("index.html")

@app.route("/api/attractions", methods=["GET"])
def attractions():
    pageNum = request.args.get("page", 0)
    pageNum = int(pageNum)
    keyword = request.args.get("keyword", "")
    
    sql = "SELECT id, name, category, description, address, transport, mrt, latitude, longitude FROM `taipeiAttractions` WHERE `name` LIKE %s ORDER BY `id` LIMIT %s, %s"
    val = (("%"+keyword+"%"), (pageNum * 12), 12)
    mycursor.execute(sql, val)

    attractions = mycursor.fetchall()

    try:
        if attractions:
            result = []
            for i in range(len(attractions)):
                data = {}
                data["id"] = attractions[i][0]
                data["name"] = attractions[i][1]
                data["category"] = attractions[i][2]
                data["description"] = attractions[i][3]
                data["address"] = attractions[i][4]
                data["transport"] = attractions[i][5]
                data["mrt"] = attractions[i][6]
                data["latitude"] = attractions[i][7]
                data["longitude"] = attractions[i][8]

                sql = "SELECT imageUrl FROM taipeiAttractionsImages WHERE imageId = %s"
                val = (str(attractions[i][0]),)
                mycursor.execute(sql, val)
                attractionsImage = mycursor.fetchall()

                imageResult = []
                for j in attractionsImage:
                    matchObj = re.search( r'jpg|png', j[0], re.I)
                    if matchObj != None:
                        imageResult.append(j[0])
                        data["images"] = imageResult

                result.append(data)

            if len(attractions) == 12:
                data = {
                    "nextPage": pageNum +1, 
                    "data": result
                }
            else:
                data = {
                    "nextPage": None, 
                    "data": result
                }
            return jsonify(data)
        else:
            data = {
                "nextPage": None, 
                "data": "no results found"
            }
            return jsonify(data)
    except:
        data = {
            "error": True,
            "message": "Error"
        }
        return jsonify(data)


@app.route("/api/attraction/<id>", methods=["GET"])
def attraction(id):
    sql = "SELECT id, name, category, description, address, transport, mrt, latitude, longitude FROM `taipeiAttractions` WHERE `id` = %s"
    val = (str(id), )
    mycursor.execute(sql, val)
    attractions = mycursor.fetchone()

    try:
        if attractions:
            result = {}
            result["id"] = attractions[0]
            result["name"] = attractions[1]
            result["category"] = attractions[2]
            result["description"] = attractions[3]
            result["address"] = attractions[4]
            result["transport"] = attractions[5]
            result["mrt"] = attractions[6]
            result["latitude"] = attractions[7]
            result["longitude"] = attractions[8]

            sql = "SELECT imageUrl FROM taipeiAttractionsImages WHERE imageId = %s"
            val = (str(id), )
            mycursor.execute(sql, val)
            attractionsImage = mycursor.fetchall()

            imageResult = []
            for row in attractionsImage:
                matchObj = re.search( r'jpg|png', row[0], re.I)
                if matchObj != None:
                    imageResult.append(row[0])
                    result["images"] = imageResult
            data = {
                "data": result
            }
            return jsonify(data)
        else:
            data = {
                "data": "No results found"
            }
            return jsonify(data)
    except:
        data = {
            "error": True,
            "message": "Error"
        }
        return jsonify(data)


@app.route("/booking")
def booking():
	return render_template("booking.html")
@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")

app.run(host="0.0.0.0", port=3000)

mycursor.close()
mydb.close()
