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

android.accept_sdk_license = True
android.api = 33
android.minapi = 21
android.ndk = 25b
android.build_tools_version = 33.0.2
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
