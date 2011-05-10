# SYNTENSITY: build runner

echo "Run this with EMSCRIPTEN=... ./build.sh"
echo "  where ... is the path to Emscripten's root directory (without a trailing '/')"
echo "  Without that, you will fail on 'compiler cannot create executables'."
echo

EMMAKEN_COMPILER=clang RANLIB=$EMSCRIPTEN/tools/emmaken.py AR=$EMSCRIPTEN/tools/emmaken.py CXX=$EMSCRIPTEN/tools/emmaken.py CC=$EMSCRIPTEN/tools/emmaken.py make -C .

