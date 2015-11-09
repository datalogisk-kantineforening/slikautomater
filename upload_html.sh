#!/bin/sh

./gen_html.py | ssh kantinen.org 'cat > slikautomater-struktur.txt'
