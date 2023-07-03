import folium
import sqlite3 as sql3

class JejuMap:
    con = sql3.connect("../Git_project/database/jeju.db")
    cur = con.cursor()

    attraction_la = cur.execute("select latitude from ATTRACTION").fetchall()
    attraction_lo = cur.execute("select longitude from ATTRACTION").fetchall()

    for attraction_gps in zip(attraction_la, attraction_lo):
        print(attraction_gps)
        print(float(attraction_gps[0][0]))

    my_map = folium.Map(location=[float(attraction_gps[0][0]),float(attraction_gps[1][0])],zoom_start=15)
    my_map.save('index.html')