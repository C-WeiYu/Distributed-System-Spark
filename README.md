# Distributed-System-Spark

## Introduction
![](img/%E6%9E%B6%E6%A7%8B%E5%9C%96.v2.png)
### Stock Data Crawler

### InfluxDB

### Spark Cluster & Regression Prediction

### Visual Design

## Dev Environment
### Spark cluster(VM - Ubuntu)
1. 先安裝好 [Vagrant](https://www.vagrantup.com/) 、 [git](https://git-scm.com/) 、[git-lfs](https://git-lfs.github.com/)

2. 執行下列命令:
```shell
git clone https://github.com/C-WeiYu/Distributed-System-Spark.git
cd Distributed-System-Spark
```
3. 透過 `Vagrantfile` 建立 spark cluster VM。(可以更改 `Vagrantfile` 的 num_nodes 設定總共要建立幾個工作節點)
```shell
vagrant up
```

4. 進入到 master 節點的 VM，啟動 master 節點。 (預設 spark-node1 為 master)
```shell
vagrant ssh spark-node1
```
```shell
sudo $SPARK_HOME/sbin/start-master.sh
```

5. 依序進入到 worker 節點的 VM，下面以 spark-node2 為例。 (預設 spark-node2、spark-node... 為 worker)

```shell
vagrant ssh spark-node2
```
```shell
sudo $SPARK_HOME/sbin/start-worker.sh spark://$MASTERIP:7077
```
6. 可以到 local 的電腦，進到 http://10.0.1.101:8080/ 去監控 VM 中的 Spark cluster。(10.0.1.101 為 master-node IP)

![](img/sparkUI.png)

7. 安裝所需的 python 套件

```shell
sudo pip3 install -r requirements.txt
```

### InfluxDB(AWS)


### Local computer(Win10)
1. 建立乾淨的 python 環境。(conda 為例也可以使用 virtualenv)
```shell
conda create --name env python=3.6
conda activate env
```

2. 安裝需要的套件。
```shell
pip install -r requirements.txt
```

### Version info 
|軟體|版本|網址|備註|
|:-:|-|-|-|
|JAVA| JDK8(linux、x86 64bit)| [OpenLogic’s OpenJDK Downloads](https://www.openlogic.com/openjdk-downloads?field_java_parent_version_target_id=416&field_operating_system_target_id=426&field_architecture_target_id=391&field_java_package_target_id=396) | 可使用: Java 8/11, Scala 2.12/2.13|
|Spark| 3.2.1(hadoop3.2) | [Downloads \| Apache Spark](https://spark.apache.org/downloads.html) ||
|Python| 3.6+ |||
|Vagrant| 2.2.19 | [Vagrant by HashiCorp (vagrantup.com)](https://www.vagrantup.com/) | 需先自行安裝 |
|Ubuntu| Ubuntu 18.04.6 LTS (Bionic Beaver) | [Discover Vagrant Boxes - Vagrant Cloud (vagrantup.com)](https://app.vagrantup.com/boxes/search?utf8=%E2%9C%93&sort=downloads&provider=&q=ubuntu%2Fbionic64+) | 透過 vagrant 安裝 |
|InfluxDB||||

## Quick start


## Demo


## reference
- Spark 叢集(Standalone Mode)
  - 官方說明
      - https://spark.apache.org/docs/latest/cluster-overview.html
      - https://spark.apache.org/docs/latest/spark-standalone.html
  - spark 叢集的設定
      - [How to Install Spark on Ubuntu {Instructional guide} (phoenixnap.com)](https://phoenixnap.com/kb/install-spark-on-ubuntu)
      - [Set up a local Spark cluster step by step in 10 minutes | by Andrew Zhu | CodeX | Medium](https://medium.com/codex/setup-a-spark-cluster-step-by-step-in-10-minutes-922c06f8e2b1)
  - vagrant 自動化部屬範例
      - [qzchenwl/vagrant-spark-cluster: Vagrantfile to setup 2-node spark cluster (github.com)](https://github.com/qzchenwl/vagrant-spark-cluster)
      - [02 setting up spark cluster with vagrant - 哔哩哔哩 (bilibili.com)](https://www.bilibili.com/read/cv10928420)
      - [vagrant学习笔记 - provision - Pekkle - 博客园 (cnblogs.com)](https://www.cnblogs.com/pekkle/p/9547111.html)
  - Ruby (vagrantfile)
    - [Ruby 程式語言入門 - Rails 實戰聖經 (ihower.tw)](https://ihower.tw/rails/ruby.html)
    - [Ruby 教程 | 菜鸟教程 (runoob.com)](https://www.runoob.com/ruby/ruby-tutorial.html)
- 爬蟲


- influxdb

- 視覺化 Dashboard
    - plotly + Dash
      - [初學Pandas+Plotly+Dash大禮包](https://weilihmen.medium.com/%E5%88%9D%E5%AD%B8pandas-ploty-dash%E5%A4%A7%E7%A6%AE%E5%8C%85-8661c04e67b7)
## Contributors
|組員|系級|學號|工作分配|github|
|-|-|-|-|:-:|
|莊崴宇|資科碩一|110753117| 簡報、github | [C-WeiYu](https://github.com/C-WeiYu)|
|何彥南|資科碩一|110753202| Spark 叢集、github | [aaron1aaron2](https://github.com/aaron1aaron2)|
|姚惠馨|資科碩一|110753135| Dashboard | [Hsin0705](https://github.com/Hsin0705)|
|吳仁凱|資科碩一|110753157| Pyspark | [k0341055](https://github.com/k0341055)|
|張修誠|資科碩一|110753165| 爬蟲 | [juzowa](https://github.com/juzowa)|
|吳泓澈|資科碩一|107306009| InfluxDB | [Hunter107306009](https://github.com/Hunter107306009)|

