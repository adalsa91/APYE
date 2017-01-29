# -*- mode: ruby -*-
# vi: set ft=ruby :

require 'yaml'

#Variables
current_dir = File.dirname(File.expand_path(__FILE__))
vars = YAML.load_file("#{current_dir}/vars.yaml")

Vagrant.configure("2") do |config|
  #Box base de Vagrant para trabajar con Azure
  config.vm.box = "azure"
  config.vm.box_url = "https://github.com/msopentech/vagrant-azure/raw/master/dummy.box"

  #Configuración ssh usada por Vagrant apra acceder a la MV
  config.ssh.username = vars["vm_user"]
  config.ssh.private_key_path = File.expand_path(vars["mgmt_certificate_path"])

  config.vm.provider :azure do |azure, override|
    #Desactivado NFS por problemas con el plugin vagrant-azure, en su lugar se usa rsync
    override.nfs.functional = false

    #Certificado personal de acceso a recursos de Azure
    azure.mgmt_certificate = File.expand_path(vars["mgmt_certificate_path"])
    azure.mgmt_endpoint = 'https://management.core.windows.net'
    azure.subscription_id = vars["azure_subscription_id"]

    #Imagen base de Ubuntu de los repositorios de Azure
    azure.vm_image = "b39f27a8b8c64d52b05eac6a62ebad85__Ubuntu-14_04_5-LTS-amd64-server-20170110-en-us-30GB"
    azure.vm_name = vars["vm_name"]
    azure.cloud_service_name = vars["vm_name"]
    azure.vm_location = 'West Europe'

    azure.vm_user = vars["vm_user"]
    azure.vm_password = vars["vm_password"]

    #Configuración ssh de la MV
    azure.ssh_port = '22'
    azure.ssh_private_key_file = File.expand_path(vars["mgmt_certificate_path"])

    #Reenvío del tráfico del puerto 80 del servicio externo al puerto 5000 de la VM
    azure.tcp_endpoints = '5000:80'
  end

  #Provisionamiento con ansible
  config.vm.provision "ansible" do |ansible|
    ansible.sudo = true
    ansible.playbook = "playbook.yaml"
    ansible.verbose = "v"
    ansible.host_key_checking = false
  end
end
