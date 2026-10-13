[app]
title = Amar Belkuri
package.name = amarbelkuri
package.domain = org.amarbelkuri
source.dir = .
source.include_exts = py
version = 1.0
requirements = python3,kivy,pyjnius,android
orientation = portrait
fullscreen = 0
android.permissions = INTERNET
android.api = 33
android.minapi = 24
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a
android.accept_sdk_license = True
p4a.branch = develop

[buildozer]
log_level = 2
warn_on_root = 1
