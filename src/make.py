#!/usr/bin/python

'''
SYNTENSITY: build runner. See README.markdown.

Note: You should do make clean and make distclean in src/enet, if you built natively before.
'''

import os, sys
from subprocess import Popen, PIPE, STDOUT

exec(open(os.path.expanduser('~/.emscripten'), 'r').read())

try:
  EMSCRIPTEN_ROOT
except:
  print "ERROR: Missing EMSCRIPTEN_ROOT (which should be equal to emscripten's root dir) in ~/.emscripten"
  sys.exit(1)

exec(open(os.path.join(EMSCRIPTEN_ROOT, 'tools', 'shared.py'), 'r').read())

stage_counter = 0
def stage(text):
  global stage_counter
  stage_counter += 1
  text = 'Stage %d: %s' % (stage_counter, text)
  print
  print '=' * len(text)
  print text
  print '=' * len(text)
  print

stage('C++ => LLVM binary')

env = os.environ.copy()
env['CXXFLAGS'] = '-g -DSYNTENSITY'
env['CC'] = env['CXX'] = env['RANLIB'] = env['AR'] = os.path.join(EMSCRIPTEN_ROOT, 'tools', 'emmaken.py')
Popen(['make', 'client'], env=env).communicate()

assert os.path.exists('sauer_client'), 'Failed to create client'

stage('Link')

Popen([LLVM_LINK, 'sauer_client', os.path.join('enet', '.libs', 'libenet.a'), '-o=client.o']).communicate()

stage('LLVM binary => LL assembly')

Popen([LLVM_DIS] + LLVM_DIS_OPTS + ['client.o', '-o=client.ll']).communicate()

assert os.path.exists('client.ll'), 'Failed to create client assembly code'

# XXX Only saves 1%, and causes a failure later, so disabling
#stage('Dead function elimination')
#Popen([os.path.join(EMSCRIPTEN_ROOT, 'tools', 'dead_function_eliminator.py'), 'client.ll', 'client.dfe.ll']).communicate()

stage('Emscripten: LL assembly => JS')

settings = {
  #'USE_TYPED_ARRAYS': 2,
  'SAFE_HEAP': 2,
  'SAFE_HEAP_LINES': ['tools.h:364'] # execute() on vectors of i32 can contain i8's as strings. Need to fix this for q1 opt
}
Popen(['python', os.path.join(EMSCRIPTEN_ROOT, 'emscripten.py'), 'client.ll', str(settings).replace("'", '"')], stdout=open('client.js', 'w'), stderr=STDOUT).communicate()

assert os.path.exists('client.js'), 'Failed to create client script code'

print 'Results of emscripten appear in client.js (both code and errors, if any)'

