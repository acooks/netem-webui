netem-webui
===========

A simple, stand-alone web interface for configuring netem parameters

### Dependencies:
	python-flask

### Start the web app:
	sudo python main.py

### Connect to the web app:
	http://localhost:8080/

### TODO:
* Describe the format for the input fields.
* Implement zero as a valid input, eg. non-zero fixed delay / zero jitter / zero loss OR eg. zero delay / non-zero jitter / zero loss, etc.
* Draw the delay, jitter, loss matrices! :D
