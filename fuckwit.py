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

class ExecutionEngine(object):
  def __init__(self, ops = None, memsize = 30000):
    object.__init__(self)

    self.mem = mem = np.ndarray(memsize, dtype=np.uint8)
    self.memsize = memsize
    self.ip = 0
    self.mp = 0
    self.ops = []

    if ops:
      self.addops(ops)

    self.handlers = [self.val, self.ptr, self.jmp, self.inp, self.out]

  def addops(self, ops):
    self.ops += ops

  def run(self):
    while self.ip != len(self.ops):
      self.handle(self.ops[self.ip])

  def handle(self, op):
    self.handlers[op[0]](*op[1:])
    self.ip += 1

  def val(self, delta):
    self.mem[self.mp] += delta

  def ptr(self, delta):
    self.mp = (self.mp + delta) % self.memsize

  def jmp(self, cond, delta):
    if (self.mem[self.mp] == 0) == cond:
      self.ip += delta

  def inp(self):
    self.mem[self.mp] = getch()

  def out(self):
    c = self.mem[self.mp]
    if c > 31 and c < 127:
      sys.stdout.write(chr(c))
    elif c == 10 or c == 13:
      sys.stdout.write('\n')

fp = open(sys.argv[1])
dat = fp.read()
fp.close()

ops = parser.parse(dat)

ee = ExecutionEngine(ops)
ee.run()