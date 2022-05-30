# -*- mode: ruby -*-
# vagrant box add my-box bionic-server-cloudimg-amd64-vagrant.box # 先載下來裝比較快，bionic64 資源 https://app.vagrantup.com/ubuntu/boxes/bionic64
# $ vagrant box add mybox
Vagrant.configure("2") do |config|
  $num_nodes = 2
  (1..$num_nodes).each do |i|
    config.vm.define "spark-node#{i}" do |node| # VM 名稱

      node.vm.box = "ubuntu/bionic64" #使用的映像檔(Ubuntu 18.04)， 會動態載
      # node.vm.box = "qzchenwl/centos"

      node.vm.synced_folder ".", "/vagrant", type: "virtualbox"

      ip = "10.0.1.#{i+100}"
      node.vm.hostname = "spark-node#{i}"
      node.vm.network "private_network", ip: ip

      node.vm.provider "virtualbox" do |vb|
        vb.memory = "2048"
        vb.cpus = 1
        vb.name = "spark-node#{i}"
      end

      node.vm.provision "file", source: "keys/id_rsa", destination: "$HOME/.ssh/id_rsa"
      node.vm.provision "file", source: "keys/id_rsa.pub", destination: "$HOME/.ssh/id_rsa.pub"
      node.vm.provision "shell", privileged: false, inline: <<-SCRIPT
          cat $HOME/.ssh/id_rsa.pub >> $HOME/.ssh/authorized_keys
      SCRIPT
      node.vm.provision "shell", path: "scripts/bootstrap.sh", args: [ip]

      if i == 1
        puts "spark-node#{i} is master"
        node.vm.provision "shell", path: "scripts/init-master.sh"
      else
          puts "spark-node#{i} is worker"
      end

    end
  end
end