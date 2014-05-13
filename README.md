# cmus-remote web app

This is a web app to control a server instance of [`cmus`](http://cmus.sf.net),
a powerful music player, remotely. So far it only supports basic player and
volume controls, not adding items to the playlist. 

![Screenshot of cmus_app running in Firefox](cmus-app-screenshot.png)

## Dependencies

- Python (tested with 2.7)
- [`bottle`](http://bottlepy.org)
- [`sh`](http://amoffat.github.com/sh/)

The web app also makes use of [Zepto](http://zeptojs.com/),
[Kube](http://imperavi.com/kube), and [Font
Awesome](http://fortawesome.github.com/Font-Awesome/). These are all included.
Thanks to the creators for making them available under permissive licenses. 

## Instructions

The web app can run on the same host as the `cmus` instance you want to control
or a different one, but both hosts will have to have `cmus` installed.

### On the web app host

- Install `bottle` and `sh` and fetch cmus_app.

        $ pip install bottle sh
        $ git clone git://github.com/jboynyc/cmus_app

- Edit the configuration file.
- Run the app:

        $ cd cmus_app
        $ python app.py [config-file]

### On the cmus host

- Run an instance of `cmus` using the `--listen` option.

        $ cmus --listen <host>

- Set a password in `cmus` using `:set passwd=<passwd>`.

### Anywhere on your network

- Open your browser and navigate to `http://<host>:<port>`.

Enjoy!

---

See Prior Art/Alternatives on the [cmus wiki](https://github.com/cmus/cmus/wiki/remote-control)
