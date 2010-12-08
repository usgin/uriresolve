-------------------------------------------------------
- BASIC INSTALLATION INSTRUCTIONS                               
-------------------------------------------------------
Prerequisites:
- A functioning Django Project

Steps:
1. Put the uriresolve folder into your project: from your project directory, 
	git clone git://github.com/azgs/uriresolve.git
2. In your project's settings.py, add 'uriresolve' to your list of INSTALLED_APPS
3. Add .../uriresolve/templates to your list of TEMPLATE_DIRS, or else symlink 
	/uriresolve/templates/uriresolve into a location already specified.
4. Add .../uriresolve/media/uriresolve to the directory specified as your MEDIA_ROOT.
	This can be done through copy/paste or symlink.
5. Add the following line to your patterns in your project's urls.py:
	(r'^uri-gin/', include('uriresolve.urls')),
6. Run 'python manage.py syncdb'