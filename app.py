#!/bin/env python2.7
from bottle import route, post, run, request, view, static_file
from sh import cmus_remote

### configuration start
host1  = 'raspberry'  # host running cmus (with --listen)
passwd = 'UnSaFe'     # password for cmus (use :set passwd=)
host2  = 'localhost'  # host running web app
port   = 8080         # port for web app
### configuration end

Remote = cmus_remote.bake('--server', host1,'--passwd', passwd) 

@route('/')
@view('main')
def index():
    return dict(host=host1)

@post('/cmd')
def run_command():
    legal_commands = ['player-play', 'player-stop', 'player-next', 'player-prev', 'vol +5', 'vol -5', 'vol 0', 'status']
    command = request.POST.get('command', default=None)
    if command in legal_commands:
        out = Remote('-C', command) 
        return {'command':command, 'result':out.exit_code, 'output':out.stdout}
    else:
        pass

@route('/static/<file>')
def static(file):
    return static_file(file, root='static')

if __name__ == '__main__':
    #debug(True)
    run(host=host2, port=port)

