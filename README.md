# Ultramarine Tweaks

The Ultramarine Tweaks app is a settings app for Ultramarine Linux

It is a system settings app that allows you to configure your Ultramarine Linux system.

Ultramarine Tweaks is fully modular and one can also add their own settings module for it.

The app is written in Python and uses GTK+3 and libhandy.


## Features

- Modular settings modules
- Python-based module system, loading modules from a directory

## Building

Ultramarine Tweaks uses some GTK and DBus libraries. You need to have those libraries installed on your system.

```
sudo dnf install gtk3-devel python3-dbus libhandy-devel
```

For Snapper support, also install Snapper.

To build, use Meson.
```
meson builddir
meson install -C builddir
```