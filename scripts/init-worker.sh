# #!/bin/bash
set -xe

sudo chown -R vagrant:vagrant /root/ # 把資料夾權限轉移，方便後續存取

cat /share/key/id_rsa.pub >> /root/.ssh/authorized_keys 