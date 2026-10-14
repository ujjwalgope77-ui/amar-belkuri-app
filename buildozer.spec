[app]
title = Amar Belkuri
package.name = amarbelkuri
package.domain = org.amarbelkuri
source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,json,html,css,js,ttf
version = 1.0
requirements = python3,kivy==2.3.0,requests,urllib3,chardet,idna,certifi,openssl,pyjnius,android
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
