# ============================================
# Author: yen-nan ho
# Github: https://github.com/aaron1aaron2
# Date: 2022.06.09
# ============================================

# #!/bin/bash

set -xe

shareFolder=$1

sudo chown -R vagrant:vagrant /root/ # 把資料夾權限轉移，方便後續存取

echo -e "\n\n\n" | ssh-keygen # 三次 enter

sudo mkdir -p /share/key # -p 如果不存在才建立

sudo cp -f /root/.ssh/id_rsa.pub $shareFolder/key/id_rsa.pub
sudo cp -f /root/.ssh/id_rsa.pub /root/.ssh/authorized_keys