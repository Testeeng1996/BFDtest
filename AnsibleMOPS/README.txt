READ ME
To successfully invoke the playbook via the Flask API in this code the following steps must take place:

1. Install Linux.
	- Install Ubuntu or use wsl --install on your local computer.
	- wsl requires an update prior to installation via wsl --update
	- Once you have updated and installed wsl you should be redirected to the shell you are using
	- If not just enter wsl into the command line on your local cmd prompt or even GitBash although command prompt works better.

2. Install Ansible
	- Ansible requires linux to run you can't just use the normal Windows shell hence the previous installation of linux.
	- Once you have installed linux do:
	
			sudo apt update
			sudo apt install ansible

		This should work to install it on your linux shell.
	- Check if it is installed by looking at the version:
	
		ansible --version
		
		And it should print what the version is. If it prints nothing or doesn't recognise it there is an issue with the previous installation.
		
3. Install python/ python3
	- Either should work but are required for Flask. 
	- Flask uses a python file type to run the app. 
	- First check if there is already a python on your shell because it should have either python or python3 already, especially on recent versions
	of Ubuntu which usually have python3.
			
		python3 -V
		
		OR
		
		python -V
		
	- If you already have python proceed to the next step otherwise a manual installation may be required. When using wsl it should put you
	automatically onto the latest version of Ubuntu if you don't define what distribution you want but otherwise make sure to use Ubuntu distribution if you are forced to select it for set up. 
		
4. Install pip/ pip3
	- pip generally doesn't come with Ubuntu so it is required to install. 
	sudo apt install -y python3-pip
	
5. Install Flask.
	- Update the shell with
		sudo apt update
		After each installation.
	- pip is required to install Flask rather than apt.
	
	pip3 install flask
	
	OR
	
	pip install flask
	
	
Now you have installed all the required programs. Next to run your python flask app go to the directory of the app and enter in the command line:
	
	python your_file.py
	
	OR
	
	python3 your_file.py
	
This will run the flask app and host it on a given IP you need to take not of. Also if there is an issue with the IP already being in use you will 
need to manually change the IP you are using in the file to another number... Generally I incremenet by one. It's hard to know exactly what IPs
are already being used but generally it works to just change the last two of four numbers at the end. 

On vLab, Python 2.7.5 is compatible but on your local computer use Python3 or above. 

Ensure you have the right version of Flask, which will correspond to the right version of Jinja2. To clarify, you require: 

Flask 2.0.1
Jinja 3.0.3
Python 3.10.12

Werkzeug 2.0.2

Check flask with:
flask --version

Check Jinja2 with: 
pip show jinja2 | grep Version

If flask or Jinja2 are wrong use: 

pip install Flask==2.0.1 Werkzeug==2.0.2

pip install Jinja2==3.0.3




To run my code use the following curls:

curl -X POST -H "Content-Type: application/json" -d "{\"nodeName\": \"O5RXvEPG01\", \"context\": \"sgi_nat\", \"additionalText\": \"The status of BFD session is changed to DOWN/ADMINDOWN\", \"neighbour\": \"2405:dc00:42:16e::3\"}" http://127.0.0.1:5022/run_session_down

For the BFD Session Down playbook. Note the IP is called here: http://127.0.0.1:5021/run_session_down ... At the very end. You need to make sure the IP you changed in the app is the same as what you are trying to pick up here.


curl -X POST -H "Content-Type: application/json" -d "{\"nodeName\":\"O6LXvEPG02\", \"additionalText\": \"Card Missing\", \"cardNumber\": \"26\"}" http://127.0.0.1:5022/run_card_missing
For the Card Missing playbook. Again keep track of the IPs you are using. 

For Switch Down playbook.
curl -X POST -H "Content-Type: application/json" -d "{\"deviceIP\": \"172.29.81.151\"}" http://127.0.0.1:5022/run_switch_down

Note that it will ask for the Vault Pass in the Flask Host shell which is:

pass

And then it will execute the code in the shell with the curl. 

To kill old processes use:
ps -ef | grep 'python invokeAnsible3Grace.py'

Then 
kill -9 [PROCESS ID]

