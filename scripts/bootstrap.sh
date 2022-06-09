# ============================================
# Author: yen-nan ho
# Github: https://github.com/aaron1aaron2
# Date: 2022.06.09
# ============================================

#!/bin/bash
set -xe # 印出執行的命令，執行中有問題則終止

sudo apt-get -y update 
sudo apt-get -y upgrade


# 設定 IP ====================================================
IP=$1 # 傳入的第一個參數
masterIP=$2
numNodes=$3
shareFolder=$4

sudo sed -i '/127.0.2.1\s\+spark-node/d' /etc/hosts # 刪除配對到的行。 會多一行 spark 自訂的 IP

for i in $(seq 1 $numNodes)
do
cat >> /etc/hosts << EOF
10.0.1.10$i spark-node$i spark-node$i
EOF
done

# 解除防火牆與限制 ===============================================
cat >> /etc/ssh/ssh_config << EOF
Host *
    StrictHostKeyChecking no
    UserKnownHostsFile=/dev/null
EOF

cat >> /etc/sysctl.conf << EOF
net.ipv6.conf.all.disable_ipv6 = 1
net.ipv6.conf.default.disable_ipv6 = 1
net.ipv6.conf.lo.disable_ipv6 = 1
EOF
sysctl -p

swapoff -a # 臨時禁用虛擬內存 swap 
sudo sed -i '/swap/s/^/#/' /etc/fstab # 永久禁用 swap 

# Disable firewall
sudo apt -y install firewalld
sudo systemctl stop firewalld
sudo systemctl disable firewalld

# Set SELinux in disabled mode | centos 才有
# setenforce 0
# sed -i 's/^SELINUX=enforcing$/SELINUX=disabled/' /etc/selinux/config

# pyspark 環境 ===============================================
sudo apt -y install python3-pip # sudo yum install -y python3

# sudo pip3 install pyspark 
# sudo pip3 install findspark
sudo pip3 install -r $shareFolder/requirements.txt

# spark & java 環境 ===============================================
sudo chown -R vagrant:vagrant /opt/ # 把資料夾權限轉移，方便後續存取

tar xf $shareFolder/packages/openlogic-openjdk-8u262-b10-linux-x64.tar.gz -C /opt
tar xf $shareFolder/packages/spark-3.2.1-bin-hadoop3.2.tgz -C /opt

mv -v /opt/spark-3.2{.1-bin-hadoop3.2,} # rename -> {} 裡的移掉
find /opt -depth -type d -name openlogic-openjdk-8u262-b10-linux-64 -execdir mv {} /opt/jdk-8 \;

cp /opt/spark-3.2/conf/spark-env.sh.template /opt/spark-3.2/conf/spark-env.sh
# 設定 spark 參數 | 10.0.1.101
cat >> /opt/spark-3.2/conf/spark-env.sh << EOF
SPARK_MASTER_HOST=$masterIP
SPARK_LOCAL_IP=$IP
export JAVA_HOME=/opt/jdk-8
EOF

# 設定路徑
# sudo chown -R vagrant:vagrant /etc/profile.d/ 
# cat >> /etc/profile.d/custom.sh << EOF
sudo chown -R vagrant:vagrant /home/vagrant # 把資料夾權限轉移，方便後續存取
cat >> .bashrc << EOF
#!/bin/bash
### JAVA ###
export JAVA_HOME=/opt/jdk-8
export CLASSPATH=.:$CLASSPATH:$JAVA_HOME/lib
export PATH=$JAVA_HOME/bin:$PATH

### Spark ###
export SPARK_HOME=/opt/spark-3.2
export PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin
export PYSPARK_PYTHON=/usr/bin/python3
export SPARK_LOCAL_IP=localhost

### custom ###
export MASTERIP=$masterIP
EOF

source .bashrc # 載入更新後的環境