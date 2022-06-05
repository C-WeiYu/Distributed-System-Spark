#引入influxdb套件
from influxdb import InfluxDBClient

#與DB建立連線
#InfluxDBClient(資料庫IP,資料庫PORT,帳號,密碼,DB名稱)
client = InfluxDBClient('54.180.25.155',8086,'','','stock_data')

#撈取爬蟲TABLE的資料
web_crawler_data = client.query('select * from web_crawler_data')
#撈取預測TABLE的資料
prediction_data = client.query('select * from prediction_data')

#對從爬蟲TABLE爬取的資料進行整理 並印出
print(list(web_crawler_data.get_points()))
print("------------")
#對從預測TABLE爬取的資料進行整理 並印出
print(list(prediction_data.get_points()))
print("------------")
#對從預測TABLE爬取的資料進行整理(抓出最後一個欄位的value) 並印出
print(list(prediction_data.get_points())[-1]['value'])


