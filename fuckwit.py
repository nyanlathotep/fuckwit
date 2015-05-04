#!/usr/local/bin/python

from fwyacc import parser
import sys
import numpy as np

memsize = 30000

if sys.stdin.isatty():
  try: 
    from msvcrt import getch 
  except ImportError: 
    def getch( ):
      import tty, termios
      fd = sys.stdin.fileno()
      old_settings = termios.tcgetattr(fd)
      try: 
        tty.setraw(fd)
        ch = sys.stdin.read(1) 
      finally: 
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings) 
      return ord(ch)
else:
  def getch():
    ch = sys.stdin.read(1)
    if not ch: ch = -1
    else: ch = ord(ch)
    return ch

fp = open(sys.argv[1])
dat = fp.read()
fp.close()

ops = parser.parse(dat)

mem = np.ndarray(memsize, dtype=np.uint8)
ip = 0
ptr = 0

while ip != len(ops):
  op = ops[ip]
  if op[0] == 0:
    mem[ptr] += op[1]
  elif op[0] == 1:
    ptr = (ptr + op[1]) % memsize
  elif op[0] == 3:
    mem[ptr] = getch()
  elif op[0] == 4:
    c = mem[ptr]
    if c > 31 and c < 127:
      sys.stdout.write(chr(c))
    if c == 10 or c == 13:
      sys.stdout.write('\n')
  elif op[0] == 2:
    if (mem[ptr] == 0) == op[1]:
      ip += op[2]
  ip += 1