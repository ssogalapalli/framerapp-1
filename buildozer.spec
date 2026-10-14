[app]

# (str) Title of your application
title = Tractor Mitra

# (str) Package name
package.name = tractormitra

# (str) Package domain (needed for android/ios packaging)
package.domain = com.example

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (list) List of Python modules to include, separated by commas.
requirements = python3,kivy

# (str) Presplash of the application
presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
icon.filename = %(source.dir)s/data/icon.png

# (str) Supported orientation
orientation = portrait

# (bool) Indicate if the application should be fullscreen or windowed
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET

# (int) Target Android API, should be as high as possible
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android logcat filters to use
android.logcat_filters = *:S python:D

# (bool) Use --private data in the package
android.private_storage = True

# (str) Android entry point, default is the main package.
# p4a creates a custom Java class which is used to start the app.
android.entrypoint = org.kivy.android.PythonActivity

# (str) Android package import name.
android.package_install_location = auto

# (bool) Use Kivy's default as this project is Kivy-based.
# Kivy version can be updated later.

[buildozer]
# (int) Log level (0 = quiet, 1 = info, 2 = warning, 3 = error)
log_level = 2

# (int) Display the build output
warn_on_root = 0
