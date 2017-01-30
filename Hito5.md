## Hito 5: Despliegue en instalamos
Para la realización de este hito se ha escogido el IaaS [Azure](https://azure.microsoft.com/es-es/)..

Las herramientas utilizadas para el despliegue automático han sido [Vagrant](https://www.vagrantup.com/), [Ansible](https://www.ansible.com/) y [Fabric](http://www.fabfile.org/); además de la [interfaz de línea de comandos de Azure](https://docs.microsoft.com/es-es/azure/xplat-cli-install).

### Instalación CLI Azure
En primer lugar instalamos la CLI de Azure, para ello es necesario tener instalado npm y Node.js, preferiblemente con algún gestor de versiones como [nvm](https://github.com/creationix/nvm).

Para instalar la CLI desde un paquete npm ejecutamos el siguiente comando en la terminal:

```bash
# npm install -g azure-cli
```

Si queremos tener las funciones de autocompletar de la CLI de azure en bash debemos ejecutar los siguientes comandos:

```bash
$ azure --completion >> ~/azure.completion.sh
$ echo 'source ~/azure.completion.sh' >> ~/.bash_profile
```

Para autentificarnos lanzamos el comando `azure login` que nos devolverá una url donde debemos introducir un código que también nos proporciona.

Una vez autentificados lo que haremos en primer lugar es descargar el archivo con las configuraciones de publicación, que contiene nuestras credenciales e información sobre nuestra subscripción.

```bash
$ azure account download
```

Este nos lanzará una url para descargar un archivo con la extensión **.publishsettings**. Ahora vamos a importar ese archivo.

```bash
$ azure account import *.publishsettings
```

Dado que este archivo contiene información sensible es recomendable borrarlo una vez importado.

Podamos comprobar que se ha importado correctamente.
```bash
$ azure account list
info:    Executing command account list
data:    Name             Id                                    Current  State  
data:    ---------------  ------------------------------------  -------  -------
data:    Pase para Azure  xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx  true     Enabled
info:    account list command OK
```
Apuntamos el identificador de subscripción ya que será necesario para el *Vagrantfile*.

### Certificado de gestión
Ahora necesitamos crear un certificado de gestión que nos permita autenticarnos con la API de administración de servicios de Azure classic, para ello creamos un par de claves privada/pública en formáto x509 y añadir la pública a nuestra cuenta de azure para poder crear recursos.
```bash
$ openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout ~/.ssh/azurevagrant.key -out ~/.ssh/azurevagrant.key
$ chmod 600 ~/.ssh/azurevagrant.key
$ openssl x509 -inform pem -in ~/.ssh/azurevagrant.key -outform der -out ~/.ssh/azurevagrant.cer
```

Para subir el certificado necesitamos usar el [portal de Azure clásico (ASM)](http://manage.windowsazure.com/), para ello una vez dentro del portal claśico ir a **Settings->Management Certificate->Upload** y seleccionamos la clave pública (con extensión **.cer**).


### Variables para despliegue
Para facilitar la modificación de ciertos parámetros relacionados con el depliegue se ha creado un fichero `vars.yaml` para almacenar variables que serán usadas por las diferentes herramientas involucradas en el despliegue.

```yaml
---
vm_name: apye
vm_user: apye
vm_password: SuperSecretPassword
azure_subscription_id: xxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

mgmt_certificate_path: azure.pem

db_user: apye
db_password: iDDLpkP1uv
db_name: apye

root_dir: /srv
project_name: APYE
project_repo: https://github.com/adalsa91/APYE

APP_SETTINGS: config.ProductionConfig
DATABASE_URL: postgresql://apye:iDDLpkP1uv@localhost/apye
SECRET_KEY: SuperSecretPassword
...
```

### Vagrant
Una vez creado el certificado de autenticación necesario para crear recursos en nuestra cuenta Azure desde aplicaciones externas ya podemos pasar a automatizar la creación de nuestra máquina con una herramienta como **Vagrant**.

Como primer paso instalamos Vagrant y el plugin [vargant-azure](https://github.com/Azure/vagrant-azure), debido a problemas de compatibilidad entre las últimas versiones de estos dos componentes se ha utilizado la versión [1.8.7 de Vagrant](https://releases.hashicorp.com/vagrant/1.8.7/), para instalar el plugin de azure usamos el siguiente comando:

```bash
$ vagrant plugin install vagrant-azure
```
Para crear una maquina virtual para Azure necesitamos una *box* base especial para Azure.

```bash
$ vagrant box add azure https://github.com/msopentech/vagrant-azure/raw/master/dummy.box
```

Para el despliegue de la VM con Vagrant solo será necesario crear un archivo `Vagrantfile` con la descripción de la configuración de la máquina virtual.

#### Vagrantfile
```ruby
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
```
Ahora podremos desplegar la máquina virtual en Azure con un solo comando:

```bash
$ vagrant up

Bringing machine 'default' up with 'azure' provider...
==> default: Determining OS Type By Image
==> default: OS Type is Linux
==> default: Attempting to read state for apye in apye
==> default: {:vm_name=>"apye", :vm_user=>"apye", :image=>"b39f27a8b8c64d52b05eac6a62ebad85__Ubuntu-14_04_5-LTS-amd64-server-20170110-en-us-30GB", :location=>"West Europe"}
==> default: {:cloud_service_name=>"apye", :storage_account_name=>"apyestoragedhymh", :tcp_endpoints=>"5000:80", :private_key_file=>"/home/adalsa/azure/azure_key.pem", :ssh_port=>"22", :vm_size=>"Small"}
Creating deployment...
Creating cloud service apye.
Uploading certificate to cloud service apye...
succeeded (200)
Creating Storage Account apyestoragedhymh.
succeeded (200)
Deployment in progress..
succeeded (200)
==> default: Attempting to read state for apye in apye
==> default: VM Status: ReadyRole
==> default: Machine reached state ReadyRole
==> default: VM 'apye' has been started
```
Como resultado de este comando se crearán tres elementos en neustra cuenta Azure: un servicio en la nube, una cuenta de almacenamiento y una máquina virtual.

### Ansible
Como se puede observar al final del **Vagrantfile** hay una sección para el provisionamiento de la máquina virtual mediante **Ansible**, utilizando el archivo **playbook.yaml** para la descripción de las tareas necesarias para el provisionamiento de las dependencias básicas.

Para instalarlo usamos el siguiente comando:

```bash
# pip install ansible
```

### Playbook
```yaml

---
- hosts: all
  become: yes

  tasks:
    - name: Update and upgrade apt packages
      apt: upgrade=yes update_cache=yes cache_valid_time=3600

    - name: Install basic dependencies
      apt: pkg={{ item }} state=present
      with_items:
        - build-essential
        - git
        - python3.4-dev
        - libpq-dev
        - postgresql
        - gunicorn

    - block:
      - name: Download get-pip.py
        get_url: url=https://bootstrap.pypa.io/get-pip.py dest=/tmp

      - name: Install pip
        command: "python3.4 /tmp/get-pip.py"

      - name: Copy settings file of Gunicorn
        template: src=gunicorn.j2 dest=/etc/init/gunicorn.conf
...
```

Estas tareas realizan una actualización de los repositorios y de todos los paquetes instalados, además instalan dependencias básicas del servicio como: Python3.4, PostgreSQL, pip...

También copia un fichero de configuración para crear un trabajo para **UpStart** para arrancar automáticamente el servidor Gunicorn, el fichero de configuración se rellena con algunas de las variables definidas en el archivo `vars.yaml` usando el motor de templates Jinja2.

```
description "Gunicorn APYE"

start on (filesystem) or runlevel [2345]
stop on runlevel [016]

respawn
setuid apye
setgid apye
chdir {{ root_dir }}/{{ project_name }}

env APP_SETTINGS={{ APP_SETTINGS }}
env DATABASE_URL={{ DATABASE_URL }}
env SECRET_KEY={{ SECRET_KEY }}

exec /usr/local/bin/gunicorn -b 0.0.0.0:5000 app:app
```

### Fabric
Para automatizar el despliegue y ejecución de la aplicación se utilizará la herramienta **Fabric**.

Para ello definimos algunas funciones en el fichero `fabfile.py`.

```python
import os
import yaml
from fabric.contrib.files import exists
from fabric.api import *

env.key_filename = 'azure.rsa'
env.user = 'apye'
env.hosts = ['apye.cloudapp.net']

with open('vars.yaml', 'r') as f:
    env.vars = yaml.load(f)

project_root = env.vars['root_dir'] + '/' + env.vars['project_name']

def get_repo():

    if exists(project_root + '/' + '.git'):
        run('cd {} && git pull origin master'.format(project_root))
    else:
        run('git clone {} {}'.format(env.vars['project_repo'], project_root))

def deploy():
    sudo('mkdir -p {}'.format(project_root))
    sudo('chown -R {}:{} {}'.format(env.vars['vm_user'], env.vars['vm_user'], project_root))
    with cd(project_root):
        get_repo()
        sudo('make install')
        sudo('service gunicorn restart')
```
Con la función deploy conseguimos descargar o actualizar el código fuente de la aplicación desde el repositorio de GitHub, instalar las dependencias de la aplicación y arrancar Gunicorn sirviendo la aplicación.

Para ejecutar el despliegue ejecutamos el siguiente comando:

```bash
    $ fab deploy
```

Una vez desplegada la aplicación podemos comprobar que todo funciona correctamente accediendo a la página [apye.cloudapp.net](apye.cloudapp.net)
