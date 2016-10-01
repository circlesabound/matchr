#!/bin/sh

BASEDIR=$(dirname $0)
PARSERDIR="$BASEDIR/parser"
SERVERDIR="$BASEDIR/server"
OUTPUTDIR="$BASEDIR/out"

mkdir -p "$OUTPUTDIR"

echo "Making parser"
cd "$PARSERDIR"
cmake .
make
mv "parser" "../out/parser"

cd "$(pwd)"

echo "Making server"
cd "$SERVERDIR"

echo "Done"

