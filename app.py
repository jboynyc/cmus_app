#!/usr/bin/env python
'''
https://github.com/jboynyc/cmus_app
'''
# =======================================================================
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as
#   published by the Free Software Foundation, either version 3 of the
#   License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
# =======================================================================


from optparse import OptionParser
try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import SafeConfigParser as ConfigParser
from bottle import abort, post, request, response, route, run, view, static_file
from sh import cmus_remote, ErrorReturnCode_1


class ConfigFileNotFound(IOError):
    '''Raised when the specified config file does not exist or is empty.'''
    pass


class MissingSetting(Exception):
    '''Raised when the config file is missing a required setting.'''
    pass


def read_config(config_file):
    r = {}
    try:
        config_parser = ConfigParser(inline_comment_prefixes=';')
    except TypeError:
        config_parser = ConfigParser()
    n = config_parser.read(config_file)
    if not len(n):
        raise ConfigFileNotFound(config_file)
    section = 'cmus_app'
    fields = ['cmus_host', 'cmus_passwd', 'app_host', 'app_port']
    for field in fields:
        try:
            r[field] = config_parser.get(section, field)
        except:
            raise MissingSetting(field)
    return r


@route('/')
@view('main')
def index():
    return {'host': settings['cmus_host']}


@post('/cmd')
def run_command():
    legal_commands = {'Play': 'player-play',
                      'Stop': 'player-stop',
                      'Next': 'player-next',
                      'Previous': 'player-prev',
                      'Increase Volume': 'vol +1%',
                      'Reduce Volume': 'vol -1%',
                      'Mute': 'vol 0'}
    command = request.POST.get('command', default=None)
    if command in legal_commands:
        try:
            out = Remote('-C', legal_commands[command])
            return {'result': out.exit_code, 'output': out.stdout.decode()}
        except ErrorReturnCode_1:
            abort(503, 'Cmus not running.')
    else:
        abort(400, 'Invalid command.')


@route('/status')
def get_status():
    try:
        out = Remote('-Q').stdout.decode().split('\n')
        r = {}
        play = out[0].split()[1]
        if play == 'playing':
            r['playing'] = True
        elif play == 'stopped':
            r['playing'] = False
        info = [i for i in out if i.startswith(('tag', 'set'))]
        for i in info:
            k, v = i.split()[1], i.split()[2:]
            if len(v):
                r[k] = ' '.join(v)
        return r
    except ErrorReturnCode_1:
        abort(503, 'Cmus not running.')


@route('/static/<file>')
def static(file):
    response.set_header('Cache-Control', 'max-age=604800')
    return static_file(file, root='static')


@route('/favicon.ico')
def favicon():
    response.set_header('Cache-Control', 'max-age=604800')
    return static_file('favicon.ico', root='static')


if __name__ == '__main__':
    option_parser = OptionParser()
    option_parser.add_option('-f', '--config', dest='config_file',
                             help='Location of configuration file.')
    option_parser.add_option('-c', '--cmus-host', dest='cmus_host',
                             help='Name of cmus host.',
                             default='localhost')
    option_parser.add_option('-w', '--cmus-passwd', dest='cmus_passwd',
                             help='Cmus password.',
                             default='')
    option_parser.add_option('-a', '--app-host', dest='app_host',
                             help='Name of cmus_app host.',
                             default='localhost')
    option_parser.add_option('-p', '--app-port', dest='app_port',
                             help='Port cmus_app is listening on.',
                             default=8080)
    options, _ = option_parser.parse_args()
    if options.config_file:
        settings = read_config(options.config_file)
    else:
        settings = vars(options)
    Remote = cmus_remote.bake(['--server', settings['cmus_host'],
                               '--passwd', settings['cmus_passwd']])
    run(host=settings['app_host'], port=settings['app_port'])
