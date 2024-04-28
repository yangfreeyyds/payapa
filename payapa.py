import requests
import json
import mysql.connector
import brotli

# api_url
url = "https://api-production-nokair-booksecure.ezyflight.se/api/v1/Availability/SearchShop"

#定义数据库连接
def mysqlinit():
    conn = mysql.connector.connect(
        host="154.8.165.65",
        user="payapa",
        password="123456",
        database="payapa"
    )
    return conn

#数据插入函数
def datainsert(conn, result):
    cursor = conn.cursor()
    sql_insert_query = """
                   INSERT INTO flights (fromCity, toCity, flightNumber, depTime, arrTime, currency, packageInfo, totalPrice, totalPriceWithoutTax, totalPriceAdult, totalPriceChild, totalPriceInfant, cabinGrade, seatCountTotal)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                   """

    values = [(r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8], r[9], r[10], r[11], r[12], r[13]) for r in result]
    try:
        cursor.executemany(sql_insert_query, values)
        conn.commit()
        print("Data inserted successfully")
    except Exception as e:
        conn.rollback()
        print("Error inserting data:", e)
    finally:
        cursor.close()

#数据定义函数
def dataset(ADT,CHD,INF,fromAirport,toAirport,departureDate,endDate,currency):
    payload = {
        "passengers": [
            {"code": "ADT", "count": ADT},
            {"code": "CHD", "count": CHD},
            {"code": "INF", "count": INF},
            {"code": "MOP", "count": 0}
        ],
        "routes": [
            {
                "fromAirport": fromAirport,
                "toAirport": toAirport,
                "departureDate": departureDate,
                "startDate": departureDate,
                "endDate": endDate
            }
        ],
        "currency": currency,
        "fareTypeCategories": None,
        "isManageBooking": False,
        "languageCode": "zh-cn"
    }

    return payload

#数据请求函数
def dataget(payload):
    headers = {
        "accept": "text/plain",
        "accept-encoding": "gzip,deflate,br,zstd",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "appcontext": "ibe",
        "authorization": "Bearer eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwidHlwIjoiSldUIn0..OaH0xPtVfCHtBYEYH0U1QA.7kOyq1LU6dZanXxoBe3Yv0-dHjTDed8NcNBjnTwpXOC9d7fwD494LJhR3iRhQ4t-sUbLFnRlU5jLk3-tSfs5omzaJU4Kj8RHo7ae8qQznGy0mftgVuY79visykQuzbDE5CVggPLv5cRfz9V_prMEyJxWIPq0DbJJqSu-yN8XHy0TCOyZH2tl4YXKht43jYK6nN-gWtr20x7xf4BSmDCmt579OYYLRZdZEExgvmj_SiX7ars-L9qKR-ruqSH6WyHbgZVoCwpN8XCZm4rY0OdRL2R4O1sCaFy5lKeDK0CBuWjugwzjnv7bSJP9qxV1-j98e3BrvXhgbZl6BaHDCrRJbszbK4POJoKunlQVGNODSNqB6Kw4UKUmCcmr-Rl8zoJpQeHcJ7TYM0zqoxRAUrCKylDKQvPe6jJUVboNXsq9THvOOgpeCoILZ7sckwVAWNwKsC8y2KcKhr6TjXb7QNUPi8se1hyxO9bRGqwgcwuoUXjr1AZpSJPbIqoERwBWugMQI9CY6cPYJ0uXW_nv_b6C14b9Rmc11636OgTuqyY1yOlQ44xs5A3-BWvxZF9qrvCY4aY_eImL-KlMP98Bb4f4AQ.ZVC6YRJ81T3R78iXmIzp60e0x3r9_l3xy_sQZlmQ11U",
        "content-type": "application/json;charset=UTF-8",
        "origin": "https://booking.nokair.com",
        "priority": "u=1, i",
        "referer": "https://booking.nokair.com/",
        "sec-ch-ua": "\"Chromium\";v=\"124\", \"Microsoft Edge\";v=\"124\", \"Not-A.Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "tenant-identifier": "FkDcDjsr3Po6GAHFnBh48dHff8MvWpCMfkKyXJ3WVQ7frJ68bD2ubXZDx6sPFRTW",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0",
        "x-clientversion": "0.5.68",
        "x-useridentifier": "XQMLnOYjYf6avINrhHuqAG5T3Oskvp"
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload), verify=False)

    return json.loads(response.content)

    #这个有时候需要解密，看脸了
    #if response.status_code == 200:
        #try:
            # 使用 brotli 解压缩响应内容
            #content = brotli.decompress(response.content)
            # 尝试解析 JSON 数据
            #data = json.loads(eval(content[0]))
            #return data
        #except brotli.error:
            #print("Failed to decompress Brotli data:")
            #return response.content
        #except json.JSONDecodeError:
            #print("Failed to decode JSON data:")
           # return

#数据提取函数
def dataextract(data,fromCity,toCity,currency):
    #print(data)
    routes = data.get("routes")
    n = len(routes[0]['flights'])
    result = []  # 创建一个空数组来存储提取的数据
    for i in range(0, n):
        m = len(routes[0]['flights'][i]['fareTypes'])
        seatCount_total = routes[0]['flights'][i]['fares'][0]['seatCount']
        flightNumber = routes[0]['flights'][i]['carrierCode'] + " " + routes[0]['flights'][i]['flightNumber']
        depTime = routes[0]['flights'][i]['departureDate']
        arrTime = routes[0]['flights'][i]['arrivalDate']
        for j in range(0, m):
            packgerInfo = routes[0]['flights'][i]['fareTypes'][j]['name']
            totalPrice = routes[0]['flights'][i]['fares'][j]['price']
            totalPriceWithoutTax = routes[0]['flights'][i]['fareTypes'][j]['fares'][0]['priceWithoutTax']
            cabinGrade = routes[0]['flights'][i]['fareTypes'][j]['fares'][0]['cabin']
            try:
                totalPrice_child = routes[0]['flights'][i]['fares'][j]['child']['price']
                totalPrice_adult = routes[0]['flights'][i]['fares'][j]['adult']['price']
                totalPrice_infant = routes[0]['flights'][i]['fares'][j]['infant']['price']
            except:
                totalPrice_child = 0
                totalPrice_adult = 0
                totalPrice_infant = 0

            # 将提取的数据添加到数组中
            result.append([fromCity,toCity,flightNumber, depTime, arrTime,currency, packgerInfo, totalPrice, totalPriceWithoutTax, totalPrice_adult, totalPrice_child, totalPrice_infant, cabinGrade, seatCount_total])
    return result  # 返回包含所有数据的数组


if __name__ == '__main__':
    #dataset(ADT,CHD,INF,fromAirport,toAirport,departureDate,endDate,currency)
    payload = dataset(1,1,1,'DMK','CEI','2024-04-28','2024-05-03','THB')

    fromCity = payload['routes'][0]['fromAirport']
    toCity = payload['routes'][0]['toAirport']
    currency = payload['currency']
    data = dataget(payload)

    result = dataextract(data,fromCity,toCity,currency)
    con = mysqlinit()
    datainsert(con,result)



