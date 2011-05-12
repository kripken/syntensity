#!/usr/bin/python

# SYNTENSITY: build runner. See README.markdown.

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
env['EMMAKEN_COMPILER'] = CLANG
env['CC'] = env['CXX'] = env['RANLIB'] = env['AR'] = os.path.join(EMSCRIPTEN_ROOT, 'tools', 'emmaken.py')
Popen(['make', '-j', '2'], env=env).communicate()

assert os.path.exists('sauer_client'), 'Failed to create client'

stage('LLVM binary => LL assembly')

Popen([LLVM_DIS] + LLVM_DIS_OPTS + ['sauer_client', '-o=sauer_client.ll']).communicate()

assert os.path.exists('sauer_client.ll'), 'Failed to create client assembly code'

stage('LL assembly => JS')

Popen(['python', os.path.join(EMSCRIPTEN_ROOT, 'emscripten.py'), 'sauer_client.ll'], stdout=open('sauer_client.js', 'w'), stderr=STDOUT).communicate()

assert os.path.exists('sauer_client.js'), 'Failed to create client script code'

print 'Results of emscripten appear in sauer_client.js (both code and errors, if any)'

