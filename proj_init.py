#!/usr/bin/env python3

"""
This python script must be run once whenever this project is downloaded from repo
"""

import mysite.settings

if not 'SECRET_KEY' in dir(mysite.settings):
    # Do not wish to perform import statement if settings are already initialized.
    import random
    import os.path

    NEW_SECRET_KEY = ''.join([random.SystemRandom().choice(
        'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50)])
    base_directory = os.path.dirname(os.path.abspath(__file__))
    init_file_path = os.path.join(base_directory, "mysite" , "settings" ,"__init__.py")

    with open(init_file_path, "a") as init_file:
        response = input("Would you like a development or production environment? \n> ")
        if response=="d" or "development" in response or "dev" in response:
            init_file.write("from mysite.settings.development import * \n\n")
        else :# Just default to production to avoid unintentional security issues
            init_file.write("from mysite.settings.production import * \n\n")
        
        # Write the secret key to the file
        init_file.write("SECRET_KEY = \"{}\"\n".format(NEW_SECRET_KEY))

        

