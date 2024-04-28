### 接口payapa.py   -byfree

#### 目录结构

```
├──api.json
├── Readme.md                   // help
├── payapa.py                   //爬虫代码
├── config                      // 配置
├── rsp.json                    //响应数据
```

#### 请求以及接口url

爬虫网站 ： https://www.nokair.com/

接口url：https://api-production-nokair-booksecure.ezyflight.se/api/v1/Availability/SearchShop

#### 接口规范

|     参数      |         数值          |      含义      |
| :-----------: | :-------------------: | :------------: |
|      ADT      |          int          |  成人乘客数量  |
|      CHD      |          int          |  儿童乘客数量  |
|      INF      |          int          |  婴儿乘客数量  |
|      MOP      |          int          |  其他乘客数量  |
|  fromAirport  |      varchar(10)      |     出发地     |
|   toAirport   |      varchar(10)      |     到达地     |
| departureDate | time(year-mounth-day) | 真正的开飞日期 |
|   startDate   | time(year-mounth-day) |  范围开始日期  |
|    endDate    | time(year-mounth-day) |  范围结束日期  |
|   currency    |      varchar(10)      |    货币类型    |
| languageCode  |    zh-cn(default)     |    语言类型    |

<u>详细见 api.js</u> 

#### 请求必要请求头

```
authorization: Bearer eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwidHlwIj……
```

```
x-useridentifier：XQMLnOYjYf6avINrhHuqAG5T3Oskvp
```

```
tenant-identifier：FkDcDjsr3Po6GAHFnBh48dHff8MvWpCMfkKyXJ3WVQ7frJ68bD2ubXZDx6sPFRTW
```

其他的挺好伪造，唯独这三个是必须要传的，这个网站是要登录才能查询的，后期逆向再说

#### 响应数据

##### 字段表（依据CT采样标准(W6)）

|        字段名        |     注释     |           例子           |
| :------------------: | :----------: | :----------------------: |
|       fromCity       |   出发城市   |         eg:'DMK'         |
|        toCity        |   到达城市   |         eg:'CEI'         |
|     flightNumber     |    航班号    |         eg:'102'         |
|       depTime        |   出发时间   | eg:'2024-04-25T11:15:00' |
|       arrTime        |   到达时间   | eg:'2024-04-25T12:35:00' |
|       currency       |   货币种类   |         eg:'THB'         |
|     packgerInfo      |   托运重量   |      eg:'NOK LITE'       |
|      totalPrice      |    总票价    |       eg:'2429.0'        |
| totalPriceWithoutTax |  无税总票价  |       eg:'2896.26'       |
|   totalPrice_adult   | 成年人总票价 |       eg:'2896.26'       |
|   totalPrice_child   |  孩童总票价  |       eg:'2896.26'       |
|  totalPrice_infant   |  婴儿总票价  |          eg:'0'          |
|      cabinGrade      |   舱位等级   |       eg:'ECONOMY'       |
|   seatCount_total    |  余下的座位  |          eg:'7'          |

<u>注：</u><u>单个种类乘客的总票价其总共有3种票价MRALIT00，MRAXTR00，MRAMAX00，对应的是不同的托运方式</u>