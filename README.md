# cmus-remote web app

This is a web app to remote control a server instance of
[`cmus`](http://cmus.sf.net), a powerful music player. So far it only supports
basic player and volume controls, not adding items to the playlist. 

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

- Install `bottle` and `sh`. Both are available with `pip`.
- Edit the configuration section of `app.py`.
- Run an instance of `cmus` on the specified host using the `--listen` option.
- Run the app: `$ cd cmus_app; python app.py`
- Open your browser and navigate to ``http://<host>:<port>``.

Enjoy!
