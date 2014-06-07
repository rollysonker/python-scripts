#!/usr/bin/env python

# top.py -- top command implemented use python.
#    get infomation from /proc system.
#    the main file for system info is:
#      /proc/stat /proc/<pid>/status /proc/<pid>/stam etc.

import sys
import re
import os
from optparse import OptionParser

def read_uptime():
    try:
        f_uptime = open("/proc/uptime", "r")
        line = f_uptime.readline()

        return line.split(None)
    finally:
        f_uptime.close()

def get_system_hz():
    """Return system hz use SC_CLK_TCK."""
    ticks = os.sysconf(os.sysconf_names['SC_CLK_TCK'])

    if ticks == -1:
        return 100
    else:
        return ticks

def parse_cmdline(argv):
    """Parses the command-line."""

    # get arguments
    parser = OptionParser(description='Top command script for display system '
                                       'infomation.')
    parser.add_option('-d', '--delay', dest='delay', metavar='int', default=3,
                      help='Delay time interval as: -d ss.tt (second.tenths).')
    parser.add_option('-n', '--number', dest='number', metavar='int',
                      default=0, help='Number of interations limit ad: -n number')
    parser.add_option('-u', '--user', dest='user', metavar="str",
                      default="all",
                      help='Monitor only processes with an effective UID or user name.')
    parser.add_option('-v', dest='verbose', action='store_true', default=False,
                      help='Display version information.')
    (options, args) = parser.parse_args(args=argv[1:])

    return (options, args)

def clrscr():
    """ Clear screen and move cursor to 1,1 (upper left) pos. """
    print '\033[2J\033[1;1H'

def clreol():
    """ Erases from the current cursor position to the end of the current line. """
    print '\033[K'

def delline():
    """ Erases the entire current line. """
    print '\033[2K'

def gotoxy(x, y):
    """ Moves the cursor to the specified position. """
    print "\033[%d;%dH" % (x, y)

def getpagesize():
    """ get the system pagesize from /proc/self/smaps """
    SMAPS = "/proc/self/smaps"
    size = 4
    unit = "kB"
    pattern = re.compile(r'KernelPageSize|MMUPageSize')

    if os.path.exists(SMAPS):
        try:
            f_smaps = open(SMAPS, "r")
            
            for line in f_smaps:
                m = pattern.match(line)
                if m:
                    array = re.split("\s+", line)
                    size = array[1]
                    unit = array[2]
                    break
        finally:
            f_smaps.close()
    
    if re.match("kB", unit):
        size = int(size) * 1024
    elif re.match("mB", unit):
        size = int(size) * 1024 * 1024
    elif re.match("gB", unit):
        size = int(size) * 1024 * 1024 * 1024

    return size

def main(argv):
    """ The main top entry point and loop."""
    
    options, args = parse_cmdline(argv)
    clrscr()
    size = getpagesize()
    print size

if __name__ == '__main__':
    sys.exit(main(sys.argv))

