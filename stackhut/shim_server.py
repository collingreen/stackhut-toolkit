 # Copyright 2015 StackHut Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Main interface into client stackhut code"""
import threading
import requests
import sh
from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple
from jsonrpc import JSONRPCResponseManager, dispatcher
from stackhut.utils import ServerError, NonZeroExitError, log

store = None

@Request.application
def application(request):
    # Dispatcher is dictionary {<method_name>: callable}
    # dispatcher["echo"] = lambda s: s
    # dispatcher["add"] = lambda a, b: a + b
    response = JSONRPCResponseManager.handle(request.data, dispatcher)
    return Response(response.json, mimetype='application/json')

def init(_store):
    global store
    store = _store

    def run_server():
         # start in a new thread
         log.debug("Starting StackHut helper-server")
         run_simple('localhost', 4000, application, threaded=False)

    # start server in sep thread
    threading.Thread(target=run_server, daemon=True).start()

def shutdown():
    pass

@dispatcher.add_method
def put_file(fname, make_public=False):
    return store.put_file(fname, make_public)

# File upload / download helpers
@dispatcher.add_method
def download_file(url, fname=None):
    """from http://stackoverflow.com/questions/16694907/how-to-download-large-file-in-python-with-requests-py"""
    fname = url.split('/')[-1] if fname is None else fname
    log.info("Downloading file {} from {}".format(fname, url))
    r = requests.get(url, stream=True)
    with open(fname, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
    return fname

@dispatcher.add_method
def run_command(cmd, stdin=''):
    try:
        output = sh.Command(cmd, _in=stdin)
    except sh.ErrorReturnCode as e:
        raise NonZeroExitError(output.exit_code, e.stderr)
    return output

# def run_command(cmd, stdin=''):
#     try:
#         p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#         stdout, stderr= p.communicate(input=stdin.encode())
#         exitcode = p.returncode
#     except OSError as e:
#         raise ServerError(-32002, 'OS error', dict(error=e.strerror))
#
#     if exitcode is not 0:
#         raise NonZeroExitError(exitcode, stderr.decode())
#     else:
#         return dict(stdout=stdout.decode())

# def call_files(cmd, stdin, stdout, stderr):
#     ret_val = subprocess.call(cmd, stdin=stdin, stdout=stdout, stderr=stderr)
#     return ret_val

