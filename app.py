#!/usr/bin/env python2.7
import sys
from ConfigParser import SafeConfigParser
from optparse import OptionParser
from bottle import route, post, run, request, view, response, static_file
from sh import cmus_remote


option_parser = OptionParser()
option_parser.add_option('-f', '--config', dest='config_file',
                         help='Location of configuration file.')
option_parser.add_option('-c', '--cmus-host', dest='cmus_host',
                         help='cmus host', default='localhost')
option_parser.add_option('-w', '--cmus-passwd', dest='cmus_passwd',
                         help='cmus password', default='')
option_parser.add_option('-a', '--app-host', dest='app_host',
                         help='cmus_app host', default='localhost')
option_parser.add_option('-p', '--app-port', dest='app_port',
                         help='cmus_app port', default=8080)


def read_config(config_file):
    r = {}
    config_parser = SafeConfigParser()
    n = config_parser.read(config_file)
    if not len(n):
        raise FileNotFoundError(config_file)
    section = 'cmus_app'
    required = ['cmus_host', 'cmus_passwd']
    for S in required:
        try:
            r[S] = config_parser.get(section, S)
        except:
            raise ValueError('{} does not specify {}.'.format(config_file, S))
    optional = [('app_host', r['cmus_host']), ('app_port', 8080)]
    for S in optional:
        try:
            r[S[0]] = config_parser.get(section, S[0])
        except:
            r[S[0]] = S[1]
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
            return {'result': out.exit_code, 'output': out.stdout}
        except:
            return {'result': False}
    else:
        pass


@route('/status')
def get_status():
    try:
        out = Remote('-Q').stdout.split('\n')
        r = {}
        play = out[0].split()[1]
        if play == 'playing':
            r['playing'] = True
        elif play == 'stopped':
            r['playing'] = False
        info = filter(lambda x: x if x.startswith('tag') or x.startswith('set') else None, out)
        for i in info:
            k, v = i.split()[1], i.split()[2:]
            if len(v):
                r[k] = ' '.join(v)
        return r
    except:
        pass


@route('/static/<file>')
def static(file):
    response.set_header('Cache-Control', 'max-age=604800')
    return static_file(file, root='static')


@route('/favicon.ico')
def favicon():
    response.set_header('Cache-Control', 'max-age=604800')
    return static_file('favicon.ico', root='static')


if __name__ == '__main__':
    options, _ = option_parser.parse_args()
    if options.config_file:
        settings = read_config(config_file)
    else:
        settings = vars(options)
    Remote = cmus_remote.bake(['--server', settings['cmus_host'],
                               '--passwd', settings['cmus_passwd']])
    run(host=settings['app_host'], port=settings['app_port'])
