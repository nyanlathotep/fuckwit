#!/usr/local/bin/python

import ply.yacc as yacc
from fwlex import tokens

def p_ops_op_reduce(p):
  'ops : ops op'
  p[0] = p[1] + [p[2]]

def p_ops_op(p):
  'ops : op'
  p[0] = [p[1]]

def p_ops_loop(p):
  'ops : ops LOOPS ops LOOPE'
  d = len(p[3])+1
  p[0] = p[1] + [[2, True, d]] + p[3] + [[2, False, -d]]

def p_op_val(p):
  'op : val'
  p[0] = p[1]

def p_op_ptr(p):
  'op : ptr'
  p[0] = p[1]

def p_val_ID_reduce(p):
  '''val : val INCR
         | val DECR'''
  p[0] = [p[1][0], p[1][1] + p[2]]

def p_val_ID(p):
  '''val : INCR
         | DECR'''
  p[0] = [0, p[1]]

def p_ptr_FB_reduce(p):
  '''val : ptr FRWD
         | ptr BKWD'''
  p[0] = [p[1][0], p[1][1] + p[2]]

def p_ptr_FB(p):
  '''ptr : FRWD
         | BKWD'''
  p[0] = [1, p[1]]

def p_op_IN(p):
  'op  : IN'
  p[0] = [3]

def p_op_OUT(p):
  'op  : OUT'
  p[0] = [4]

def p_error(p):
  if p == None:
    raise SyntaxError, 'unexpected end of file while parsing'
  elif p.type == "LOOPE":
    raise SyntaxError, 'mismatched ]'
  else:
    raise SyntaxError, 'unknown syntax error, ' + str(p)

parser = yacc.yacc()

if __name__ == '__main__' :
  fp = open('hello.bf')
  dat = fp.read()
  fp.close()
  ops = parser.parse(dat, debug = True)
  print(ops)