***This app runs on Django version 1.3.0 which is now unsupported.  Users
should install this software into a virtual environments and install all of the 
dependencies in `pip-requirements.txt` to ensure that everything runs properly***

### Installation Notes
The structure of static files in this application is very disorganized.  All of 
the code unique to this application expects static files to be served out of the
`MEDIA_URL` variable and all of the vanilla-Django code expects static files to
be served out of the `STATIC_URL` variable.  Keep this in mind, especially if you're
more experienced with newer versions of Django where the `MEDIA_URL` exists solely 
for content (like images) and the `STATIC_URL` exists for actual static files.

1.  Either clone or symlink this django app into an existing django project.
2.  In your `settings.py` file, change the following variables:

```
DATABASES = {This will be unique to your system}
MEDIA_ROOT = '/path/or/symlink/to/uriresolve/media/resolve/'
STATIC_ROOT = '/path/or/symlink/to/uriresolve/static/'
MEDIA_URL = '/media/'
STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/static/admin/'
TEMPLATE_DIRS = '/path/or/symlink/to/uriresolve/templates/uriresolve'
INSTALLED_APPS = (
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.staticfiles',
	'django.contrib.admin',
	'uriresolve',
)
```

3. In your `urls.py` file, add these url patterns:

```
url(r'^$', 'django.views.generic.simple.redirect_to', {'url': '/uri-gin/uri-description/'}),
url(r'^admin/', include(admin.site.urls)),
url(r'^uri-gin/', include('uriresolve.urls')),
```

4.  Copy or symlink the static files from this app (.../uriresolve/media/uriresolve/) into
the `MEDIA_ROOT` folder and copy or symlink the vanilla-Django static files into the `STATIC_ROOT` folder.  The vanilla-Django static files can usually be found here:
.../lib/python2.7/site-packages/django/contrib/admin/.  Once you have your static files
sorted out, run this command:

```
python manage.py collectstatic
```

And that's it!  Otherwise, this can be managed as a regular Django application.  
Don't forget to `chmod 701` if you're serving this data with Nginx out of a folder
on the `/home/` path.