#!/usr/bin/env python2.7
import sys
from ConfigParser import SafeConfigParser
from bottle import route, post, run, request, view, response, static_file
from sh import cmus_remote

# configuration file either supplied via command line  
# or assumed to be in one of the default locations
if sys.argv > 1:
    CONFIG=sys.argv[1:]
else:
    CONFIG=['config','config.ini','.config']

def read_config(config_file):
    r = {}
    parser = SafeConfigParser()
    n = parser.read(config_file)
    if not len(n): raise(Exception('File not found: {}.'.format(config_file)))
    section = 'cmus_app'
    required = ['cmus_host', 'cmus_passwd']
    for S in required:
        try:
            r[S] = parser.get(section, S)
        except:
            raise(Exception('{} does not specify {}.'.format(config_file,S)))
    optional = [('app_host', r['cmus_host']), ('app_port',8080)]
    for S in optional:
        try:
            r[S[0]] = parser.get(section, S[0])
        except: 
            r[S[0]] = S[1]
    return r

@route('/')
@view('main')
def index():
    return {'host':settings['cmus_host']}

@post('/cmd')
def run_command():
    legal_commands = {'Play':'player-play', 'Stop':'player-stop', 'Next':'player-next', 'Previous':'player-prev', 'Increase Volume':'vol +1%', 'Reduce Volume':'vol -1%', 'Mute':'vol 0'}
    command = request.POST.get('command', default=None)
    if legal_commands.has_key(command):
        try:
            out = Remote('-C', legal_commands[command]) 
            return {'result':out.exit_code, 'output':out.stdout}
        except: 
            return {'result':False}
    else:
        pass

@route('/status')
def get_status():
    try:
        out = Remote('-Q').stdout.split('\n')
        r = {}
        play = out[0].split()[1] 
        if play == 'playing': r['playing'] = True
        elif play == 'stopped': r['playing'] = False
        info = filter(lambda x: x if x.startswith('tag') or x.startswith('set') else None, out)
        for i in info:
            k, v = i.split()[1], i.split()[2:]
            if len(v): r[k] = ' '.join(v)
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
    settings = read_config(CONFIG)
    Remote = cmus_remote.bake('--server', settings['cmus_host'],'--passwd', settings['cmus_passwd']) 
    run(host=settings['app_host'], port=settings['app_port'])

