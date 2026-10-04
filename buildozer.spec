[app]
title = KivyCalc
package.name = kivycalc
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy==2.3.0
orientation = portrait
osx.kivy_version = 2.3.0

[buildozer]
log_level = 2
warn_on_root = 1

[android]
api = 33
minapi = 21
ndk_version = 25c
archs = arm64-v8a, armeabi-v7a
permissions = INTERNET
