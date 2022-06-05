#引入influxdb套件
from influxdb import InfluxDBClient

#與DB建立連線
#InfluxDBClient(資料庫IP,資料庫PORT,帳號,密碼,DB名稱)
client = InfluxDBClient('54.180.25.155',8086,'','','stock_data')

update_content1="18020000,526.44,529.0,18,16.0,3.11,530.0,530.0,522.0,524.0,530.0,708,14669902147,27866,34,0.98,28327,2022-05-27,14:30:00.000,2330,1"
#measurement為TABLE名稱 / topic為欄位名稱 / value為存入的值
web_crawler_data = [
			{
				"measurement" : "web_crawler_data",
				"tags" : {
					"topic":"stock2330_data"
				},
				"fields":{
					"value": update_content1
				}
			}
		]

#將測試資料存入爬蟲TABLE
client.write_points(web_crawler_data)

update_content2="47840000,524.65,520.0,1808,-8.0,-1.52,520.0,531.0,520.0,530.0,521.0,28,9339815468,17802,92,1.04,17054,2022-05-24,14:30:00.000,2330,2"
#measurement為TABLE名稱 / topic為欄位名稱 / value為存入的值
prediction_data = [
			{
				"measurement" : "prediction_data",
				"tags" : {
					"topic":"stock2330_data"
				},
				"fields":{
					"value": update_content2
				}
			}
		]

#將測試資料存入預測TABLE
client.write_points(prediction_data)