# Udacity Full Stack Nanodegree Project: Multi User Blog

A multi-user blog built in Python 2.7 on Google Cloud's Google App Engine. This project features the webapp2 python web framework, jinja2 templating system, and Google Cloud's Datastore API. In addition, I have chosen to also use the following library/frameworks:

-[Markdown](https://pypi.python.org/pypi/Markdown) - Python implementation of the Markdown markup language for richer text.  
-[py-bcrypt](https://pypi.python.org/pypi/py-bcrypt/0.4) - A hashing library for secure passwords  
-[jQuery](http://www.jquery.com) - Javascript library for quick and easy DOM manipulation and event handling  
-[Bootstrap](http://getbootstrap.com/) - CSS Framework for quick and easy basic grid layout and css elements

The live version of this website can be found at:  
http://kenkjw-udacity-p03.appspot.com


Instructions for deploying app: 
* [Install Python](https://www.python.org/downloads/) if necessary. 
* [Install Google App Engine SDK.](https://cloud.google.com/appengine/downloads#Google_App_Engine_SDK_for_Python)
* Sign Up for a [Google App Engine Account.](https://console.cloud.google.com/appengine/)
* Create a new project in [Google’s Developer Console](https://console.cloud.google.com/) using a unique name.
* Configure your gcloud to use the new project with `gcloud init`
* Navigate to your project directory with app.yaml and deploy your project with `gcloud app deploy`.

To run the app locally, use `dev_appserver.py {project_dir}`