# passion-blog
Personal website built using Django, containing simple blog app

In order to get started deploying this, follow these easy steps!

1.  Have python 3.x installed, along with your favorite virtual environment (I recommend virtualenvwrapper)

2.  Clone repo and in cloned directory, activate your virtual environment if you're using one, and run commands
	
	$ pip install -r requirements.txt
	
	$ python proj_init.py
	    
    $ python manage.py migrate

	$ python manage.py collectstatic

	And, if you wish to have an admin user in order to create regular users or edit blog posts and the like
	(You probably do want this)

	$ python manage.py createsuperuser

3.  Congratulations, you are now good to go!
