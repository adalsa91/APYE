
install:
	pip install -r requirements.txt

test:
	python3.4 -m unittest discover

run:	
	python3.4 manage.py runserver --host 0.0.0.0

deploy-azure:
	sudo apt-get update
	FILE=`mktemp`; wget https://releases.hashicorp.com/vagrant/1.8.7/vagrant_1.8.7_x86_64.deb -qO $FILE && sudo dpkg -i $FILE; rm $FILE
	vagrant plugin install vagrant-azure
	FILE=`mktemp`; wget https://bootstrap.pypa.io/get-pip.py -q0 $FILE && sudo python get-pip.py; rm $FILE
	sudo pip install ansible fabric
	vagrant up
	fab deploy
