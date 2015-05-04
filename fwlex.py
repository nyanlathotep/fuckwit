#!/usr/local/bin/python

import ply.lex as lex

tokens = (
  "INCR",
  "DECR",
  "FRWD",
  "BKWD",
  "LOOPS",
  "LOOPE",
  "IN",
  "OUT"
)

t_LOOPS = '\\['
t_LOOPE = '\\]'
t_IN = r','
t_OUT = r'\.'
t_ignore_COMMENT = r'[^\[\]\-+<>,.]+'

def t_INCR(t):
  r'\++'
  t.value = len(t.value)
  return t

def t_DECR(t):
  r'-+'
  t.value = -len(t.value)
  return t

def t_FRWD(t):
  r'>+'
  t.value = len(t.value)
  return t

def t_BKWD(t):
  r'<+'
  t.value = -len(t.value)
  return t

def t_error(t):
  pass

lexer = lex.lex()

if __name__ == '__main__':
  fp = open('hello.bf')
  dat = fp.read()
  fp.close()
  lexer.input(dat)
  tok = lexer.token()
  while tok:
    print(tok)
    tok = lexer.token()