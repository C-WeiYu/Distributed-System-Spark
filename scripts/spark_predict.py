# coding: utf-8
"""
Author: yen-nan ho、吳仁凱
Github: https://github.com/aaron1aaron2、https://github.com/k0341055
Date: 2022.06.09
"""

import os
from sre_constants import SUCCESS

MASTER_IP = os.getenv('MASTERIP')
SPARK_HOME = os.getenv('SPARK_HOME')

import time
import argparse
import numpy as np
from datetime import datetime

import findspark
findspark.init(SPARK_HOME)

from influxdb import InfluxDBClient

from pyspark.sql import SparkSession
from pyspark.ml.regression import LinearRegression
from pyspark.ml.feature import VectorAssembler, StandardScaler
from pyspark.sql.functions import round as spround
from pyspark.ml import Pipeline


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--date", help = "缺失日期", type = str, default = '2022-06-07')
    parser.add_argument("--time", help = "缺失時間", type = str, default = '13:24:16.550')
    parser.add_argument("--his_num", help = "預測依據的筆數", type = int, default = 10)
    parser.add_argument("--his_ws", help = "預測依據的筆數", type = int, default = 3)
    
    return parser.parse_args()

def get_data(client, miss_datetime, his_num, his_ws):
    start_time = time.time()
    data_num = his_num + his_ws -1

    #撈取預測TABLE的資料
    miss_num = 5
    teststdata = []
    while len(teststdata) < data_num:
        prediction_data = client.query(f'SELECT * FROM prediction_data GROUP BY * ORDER BY DESC LIMIT {data_num + miss_num}')

        teststdata = []
        for item in list(prediction_data.get_points())[::-1]:
            dtime = datetime.strptime(' '.join(item['value'].split(' ')[-4:-2]),"%Y-%m-%d  %H:%M:%S.%f")
            if dtime < miss_datetime:
                teststdata.append(item['value'].split(' ')[6]) # 只取第 6 個 close
            if len(teststdata) >= data_num:
                break
        
        miss_num = data_num - len(teststdata)
        print(f'{miss_num} pieces of data are missing')
        time.sleep(1)
    
    # teststdata = teststdata[::-1] #反序時間成由早到晚
    teststdata.append(teststdata[-1])
    tmp = []
    for i in range(his_num + 1):
        tmp.append(teststdata[i: i + his_ws])
    teststockarr = np.array(tmp)
    teststockarr = teststockarr.astype('float32') #str to float
    stockdata = teststockarr.tolist()

    columns = list(range(-his_ws+1,0,1))
    columns = map(lambda x:'T'+str(x),columns)
    columns = list(columns)
    columns.append('T')

    return stockdata, columns, time.time() - start_time


def predict_price(miss_datetime, data, columns):
    start_time = time.time()
    # 設定SparkSession參數並建立
    spark = SparkSession.builder.master(f'spark://{MASTER_IP}:7077').appName(f'spark-predict [{miss_datetime}]').getOrCreate()
    spark.sparkContext.setLogLevel("ERROR") 

    # 建立SparkContext
    df = spark.createDataFrame(data, schema = columns)
    columns.remove('T') # Label
    # train_data, test_data = df.randomSplit([0.9, 0.1], 2) # 會亂掉
    train_data = df.limit(df.count()-2)
    test_data = df.subtract(train_data) # 確定是要預測的那筆

    #build model
    vecass = VectorAssembler(inputCols=columns, outputCol='features')
    lr = LinearRegression(featuresCol = 'features', labelCol='T', maxIter=1, regParam=0.3, elasticNetParam=0)
    lr_pipeline = Pipeline(stages=[vecass, lr])
    
    # 預測
    lr_pipelineModel = lr_pipeline.fit(train_data)
    predicted = lr_pipelineModel.transform(test_data)
    predicted = predicted.withColumn("pred", spround(predicted.prediction, 0))

    # from pyspark.ml.evaluation import RegressionEvaluator
    # predicted.select(['T','pred']).show()
    # evaluator = RegressionEvaluator(labelCol = 'T',predictionCol = 'pred', metricName = 'rmse')
    # rmse = evaluator.evaluate(predicted)
    # print('rmse :',rmse)

    #把預測結果寫入db的test表中
    try:
        result = [
            {
                "measurement" : "prediction_data",
                "tags": {
                    "topic": "stock2330_data"
                },
                "fields": {
                    "value": 'na '*6+str(predicted.collect()[-1].pred)+' na'*10 + ' ' + str(miss_datetime) + ' 2330 *'
                }
            }
        ]
        statu = True
    except:
        result = []
        statu = False

    return result, time.time() - start_time, statu

def write_data(client, result, statu):
    start_time = time.time()
    if statu:
        client.write_points(result)
        print('SUCCESS')
    else:
        print('FALSE')

    return time.time() - start_time

def main():
    print('------------- Spark running -------------')
    args = get_args()

    miss_datetime = datetime.strptime(f"{args.date} {args.time}", "%Y-%m-%d  %H:%M:%S.%f")

    client = InfluxDBClient('54.180.25.155',8086,'','','stock_data') #InfluxDBClient(資料庫IP,資料庫PORT,帳號,密碼,DB名稱)

    data, columns, DBread_timeuse = get_data(client, miss_datetime, args.his_num, args.his_ws)

    result, spark_timeuse, statu = predict_price(miss_datetime, data, columns)

    DBwrite_timeuse = write_data(client, result, statu)

    print('--- Spark_timeuse: %.2f (sec) | DBread_timeuse: %.2f (sec)| DBwrite_timeuse: %.2f (sec) | Statu: %s ---' % (
        round(spark_timeuse, 2),
        round(DBread_timeuse, 2),
        round(DBwrite_timeuse,2),
        statu))

if __name__ == "__main__":
    main()