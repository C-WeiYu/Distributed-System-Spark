# -*- mode: ruby -*-
# vagrant box add my-box bionic-server-cloudimg-amd64-vagrant.box # 先載下來裝比較快，bionic64 資源 https://app.vagrantup.com/ubuntu/boxes/bionic64
# $ vagrant box add mybox
Vagrant.configure("2") do |config|
  $num_nodes = 3 # 控制總共要幾個節點
  $masterIP = 0 # 紀錄 master 節點 ip
  $share_folder = "/home/vagrant/Distributed-System-Spark"
  (1..$num_nodes).each do |i|
    config.vm.define "spark-node#{i}" do |node| # VM 名稱

      node.vm.box = "ubuntu/bionic64" #使用的映像檔(Ubuntu 18.04)， 會動態載

      node.vm.synced_folder ".", $share_folder, type: "virtualbox"

      ip = "10.0.1.#{i+100}"
      node.vm.hostname = "spark-node#{i}"
      node.vm.network "private_network", ip: ip

      node.vm.provider "virtualbox" do |vb|
        vb.memory = "4096"
        vb.cpus = 3
        vb.name = "spark-node#{i}"
      end

      if i == 1
        puts "spark-node#{i} is master | IP:#{ip}"
        $masterIP = ip
        node.vm.provision "shell", path: "scripts/init-master.sh", args: ["#{$share_folder}"]
      else
        puts "spark-node#{i} is worker | IP:#{ip}"
        node.vm.provision "shell", path: "scripts/init-worker.sh", args: ["#{$share_folder}"]
      end

      node.vm.provision "shell", path: "scripts/bootstrap.sh", args: [ip, "#{$masterIP}", "#{$num_nodes}", "#{$share_folder}"]
    end
  end
end