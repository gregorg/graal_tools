#!/usr/bin/python -O
# -*- coding: iso-8859-1 -*-

import sys
import os
import threading
import time
import logging
import socket
import struct


# Change proc name if possible :
def set_proc_name(new_name): # {{{
	try:
		import prctl
		prctl.set_proctitle(new_name)
		prctl.set_name(new_name)
	except:
		logging.warning("Unable to set proc name %s:"%new_name, exc_info=True)

# }}}


# invert a dict
def invert(mydict): # {{{
	return dict([[v,k] for k,v in mydict.items()])

# }}}


def Detach(): # {{{
	""" Daemonize """
	# http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/278731

	logging.shutdown()
	try: 
		if os.fork() > 0:
			sys.exit(0)   # Exit first parent.
	except OSError, e: 
		sys.stderr.write ("fork #1 failed: (%d) %s\n" % (e.errno, e.strerror) )
		sys.exit(1)

	#os.chdir("/")
	# nouvelle session
	os.setsid()
	os.umask(0)
	
	# 2eme fork
	try:
		pid = os.fork()
		if pid > 0:
			# exit second parent
			sys.exit(0)
   
	except OSError, e:
		sys.stderr.write ("fork #2 failed: (%d) %s\n" % (e.errno, e.strerror) )
		sys.exit(1)

	# Resource usage information.
	import resource		
	maxfd = resource.getrlimit(resource.RLIMIT_NOFILE)[1]
	if (maxfd == resource.RLIM_INFINITY):
		maxfd = 1024
	  
	# Iterate through and close all file descriptors.
	for fd in range(0, maxfd):
		try:
			os.close(fd)
		except OSError:	# ERROR, fd wasn't open to begin with (ignored)
			pass

	# The standard I/O file descriptors are redirected to /dev/null by default.
	if (hasattr(os, "devnull")):
		REDIRECT_TO = os.devnull
	else:
		REDIRECT_TO = "/dev/null"

	# This call to open is guaranteed to return the lowest file descriptor,
	# which will be 0 (stdin), since it was closed above.
	os.open(REDIRECT_TO, os.O_RDWR)	# standard input (0)

	# Duplicate standard input to standard output and standard error.
	os.dup2(0, 1)			# standard output (1)
	os.dup2(0, 2)			# standard error (2)


# }}}


def Beep(count=1, slp=0): # {{{
	""" Emet un beep """
	try:
		cons = open ("/dev/console","a")

		for i in range(count):
			cons.write("\a")
			cons.flush()
			time.sleep(slp)
		cons.close()
	except IOError:
		pass 
	except:
		logging.warning("", exc_info=True)

# }}}


def iptoint(ip): # {{{
	return struct.unpack("!I", socket.inet_aton(ip))[0]
# }}}

if __name__ == '__main__':
	#Beep(4, 1)
	print iptoint("127.0.0.1")

