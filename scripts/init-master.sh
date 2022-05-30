#!/bin/bash
set -xe
cp /opt/spark-3.2/conf/workers.template /opt/spark-3.2/conf/slaves

cat >> /opt/spark-3.2/conf/slaves << EOF
spark-node1
spark-node2
EOF

