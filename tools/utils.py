import os, sys

def get_data_dir():
    return os.path.expanduser('~') + "/.lss"

def get_num_lines(filename):
    with open(filename, "r") as f:
        num_lines = sum(1 for i in f)
        return num_lines

def find_between_r( s, first, last ):
    try:
        start = s.rindex( first ) + len( first )
        end = s.rindex( last, start )
        return s[start:end]
    except ValueError:
        return ""

def request_root():
    euid = os.geteuid()
    if euid != 0:
        args = ['sudo', sys.executable] + sys.argv + [os.environ]
        # the next line replaces the currently-running process with the sudo
        os.execlpe('sudo', *args)
    if euid != 0:
        return 0
    return 1
