#!/usr/bin/env python3

import sys
import os.path


TYK, TYND = 'TYK', 'TYND'

if len(sys.argv) > 1:
    gen_raw = True
else:
    gen_raw = False

def parse_row_line(s):
    return list(map(lambda s: s.strip(), s.strip('|').split('|')))

def parse_row(s):
    row_lines = list(map(parse_row_line, s.split('\n')))
    row_type = row_lines[0][0]
    if row_type == 'TYK':
        row_type = TYK
    elif row_type == 'TYND':
        row_type = TYND
    else:
        raise Exception('no row type')
    row_lines = list(map(lambda l: l[1:], row_lines))
    row_lines[0] = list(map(int, row_lines[0]))
    return (row_type, row_lines)

def parse_machine(s):
    parts = s.split('\n\n')
    name = parts[0]
    rows = list(map(parse_row, parts[1:]))
    return (name, rows)

def format_machine(t):
    html = ''
    name, rows = t
    if gen_raw:
        html += '<h2>{}</h2>\n'.format(name)
    else:
        html += '===== {} =====\n\n'.format(name)
    if not gen_raw:
        html += '<HTML>\n'
    if gen_raw:
        html += '<table>\n'
    else:
        html += '<table style="font-size: 80%;">\n'
    for row in rows:
        row_type, row_lines = row
        if row_type == TYK:
            extra = ' style="font-weight: bold"'
        else:
            extra = ''
        html += '<tr{}>\n'.format(extra)
        for cell_index in range(len(row_lines[0])):
            pladsnummer = row_lines[0][cell_index]
            vare = row_lines[1][cell_index]
            pris = str(row_lines[2][cell_index])
            if pris:
                pris = ', ' + pris + ' kr.'
            if len(row_lines[0]) <= 5:
                extra = ' colspan="2"'
            else:
                extra = ''
            html += '<td{}>{}: {}{}</td>\n'.format(extra, pladsnummer, vare, pris)
        html += '</tr>\n'
    html += '</table>\n'
    if not gen_raw:
        html += '</HTML>\n'
    return html

bdir = os.path.dirname(__file__)

with open(os.path.join(bdir, 'indhold.txt')) as f:
    content = f.read()

machines = map(format_machine, map(parse_machine, content.split('\n\n\n')))

body = '\n\n'.join(machines)

if gen_raw:
    template_filename = 'skabelon.html'
else:
    template_filename = 'skabelon.txt'

with open(os.path.join(bdir, template_filename)) as f:
    template = f.read()
    
html = template.replace('{krop}', body).rstrip()

print(html)
