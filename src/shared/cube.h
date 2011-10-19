#ifndef __CUBE_H__
#define __CUBE_H__

#ifdef __GNUC__
#define gamma __gamma
#endif

#ifdef WIN32
#define _USE_MATH_DEFINES
#endif
#include <math.h>

#ifdef __GNUC__
#undef gamma
#endif

#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <stdarg.h>
#include <limits.h>
#include <assert.h>
#include <time.h>

#ifdef WIN32
  #define WIN32_LEAN_AND_MEAN
  #define _WIN32_WINNT 0x0500
  #include "windows.h"
  #ifndef _WINDOWS
    #define _WINDOWS
  #endif
  #ifndef __GNUC__
    #include <eh.h>
    #include <dbghelp.h>
  #endif
  #define ZLIB_DLL
#endif

#ifndef STANDALONE
#include <SDL.h>
#include <SDL_image.h>

#define GL_GLEXT_LEGACY
#define __glext_h__
#define NO_SDL_GLEXT
#if !SYNTENSITY
  #include <SDL_opengl.h>
  #undef __glext_h__
  #include "GL/glext.h"
#else
typedef int GLuint;
typedef int GLenum;
#define GL_FALSE 0
#define GL_TRUE 1
#define GL_RGB 177
#define GL_TEXTURE_2D 188
#endif
#endif

#include <enet/enet.h>

#include <zlib.h>

#ifdef __sun__
#undef sun
#undef MAXNAMELEN
#ifdef queue
  #undef queue
#endif
#define queue __squeue
#endif

#include "tools.h"
#include "geom.h"
#include "ents.h"
#include "command.h"

#include "iengine.h"
#include "igame.h"

#endif

