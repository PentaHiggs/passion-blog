#!/usr/bin/env python3
"""
This python script must be run once whenever this project is downloaded from repo
"""

import_fail = False

try:
	import mysite.settings
	if not 'SECRET_KEY' in dir(mysite.settings):
		import_fail = True
except ImportError:
	import_fail = True

if import_fail:
	# Do not wish to perform import statement if settings are already initialized.
	import random
	import os.path

	NEW_SECRET_KEY = ''.join([random.SystemRandom().choice(
        'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50)])
	base_directory = os.path.dirname(os.path.abspath(__file__))
	init_file_path = os.path.join(base_directory, "mysite" , "settings" ,"__init__.py")

	with open(init_file_path, "w") as init_file:
		setup_type = "development"
		response = input("Would you like a development or production environment? \n> ")
		if response=="d" or "development" in response or "dev" in response:
			init_file.write("from mysite.settings.development import * \n\n")
		else :# Just default to production to avoid unintentional security issues
			setup_type = "production"
			init_file.write("from mysite.settings.production import * \n\n")
			response = input("Would you like to associate any domain names or IP addresses" +
				" with your Django server?  y/n\n> ")
			if response =="y":
				allowed_hosts = "ALLOWED_HOSTS += ["
				print("Please type domain names and IP addresses below.  Type empty"
							+" line to end")
				while True:
					response = input("> ")
					if not response=="":
						allowed_hosts += " \"{}\",".format(response)
					else: #empty response
						break

				allowed_hosts += "] \n"
				init_file.write(allowed_hosts)	

        # Write the secret key to the file
		init_file.write("SECRET_KEY = \"{}\"\n".format(NEW_SECRET_KEY))
		print("Django SECRET_KEY set.")
		print("Django {} environment setup complete!".format(setup_type)) 
