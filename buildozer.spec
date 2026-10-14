[app]
title = Amar Belkuri
package.name = amarbelkuri
package.domain = org.amarbelkuri
source.dir = .
source.include_exts = py,png,jpg,kv
source.exclude_dirs = templates,static,.github,bin,.buildozer
icon.filename = %(source.dir)s/icon.png
version = 1.0
requirements = python3,kivy==2.3.0,pyjnius,android
orientation = portrait
fullscreen = 0
android.permissions = INTERNET
android.api = 33
android.minapi = 24
android.ndk = 25b
android.archs = arm64-v8a
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
