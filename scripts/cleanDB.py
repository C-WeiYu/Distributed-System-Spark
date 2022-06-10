"""
Author: yen-nan ho
Github: https://github.com/aaron1aaron2
Date: 2022.06.10
"""
from influxdb import InfluxDBClient
client = InfluxDBClient('54.180.25.155',8086,'','','stock_data')


_ = client.query('drop measurement web_crawler_data')
_ = client.query('drop measurement prediction_data')
