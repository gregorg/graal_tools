#!/usr/bin/python -O
# -*- coding: iso-8859-1 -*-

import logging
import logging.handlers
import os, re, sys, threading

try:
	import termcolor
except ImportError:
	logging.warning("You can have colors with 'termcolor'")


def setup_logging(debug_level=None, threadless=False, logfile=None, rotate=False): # {{{
	# if threadless mode, it's a workarround for new Process
	if threadless or rotate:
		try:
			logfile = logging.root.handlers[0].baseFilename

			if rotate:
				try:
					logging.root.handlers[0].close()
					# rotate handled by logrotate
				except:
					print "Unable to close file:"
					print sys.exc_value
		except AttributeError: logfile=None

		# removing them with technic to not need lock :
		# see line 1198 from /usr/lib/python2.6/logging/__init__.py
		while len(logging.root.handlers) > 0:
			logging.root.handlers.remove(logging.root.handlers[0])

		if debug_level is None:
			debug_level = logging.root.getEffectiveLevel()
	else:
		# ensure closed
		logging.shutdown()
		if debug_level is None:
			debug_level = logging.DEBUG

	if logfile:
		loghandler = logging.handlers.WatchedFileHandler(logfile)
	else:
		loghandler = logging.StreamHandler()

	loghandler.setLevel(debug_level)
	#loghandler.setFormatter(logging.Formatter(logformat, logdatefmt))
	use_color = False
	if os.environ.has_key("TERM") and ( re.search("term", os.environ["TERM"]) or os.environ["TERM"] in ('screen',) ):
		use_color = True
	loghandler.setFormatter(ColoredFormatter(use_color))

	while len(logging.root.handlers) > 0:
		logging.root.removeHandler(logging.root.handlers[0])

	logging.root.addHandler(loghandler)
	logging.root.setLevel(debug_level)
# }}}


class ColoredFormatter(logging.Formatter): # {{{
	COLORS = {
		'WARNING': 'yellow',
		'INFO': 'cyan',
		'CRITICAL': 'white',
		'ERROR': 'red'
	}
	COLORS_ATTRS = {
		'CRITICAL': 'on_red',
	}

	def __init__(self, use_color = True):
		# main formatter:
		logformat = '%(asctime)s %(threadName)14s.%(funcName)-15s %(levelname)-8s %(message)s'
		logdatefmt = '%H:%M:%S %d/%m/%Y'
		logging.Formatter.__init__(self, logformat, logdatefmt)
		
		# for thread-less scripts :
		logformat = '%(asctime)s %(module)14s.%(funcName)-15s %(levelname)-8s %(message)s'
		self.mainthread_formatter = logging.Formatter(logformat, logdatefmt)

		self.use_color = use_color
		if self.use_color and not 'termcolor' in sys.modules:
			logging.debug("You could activate colors with 'termcolor' module")
			self.use_color = False

	def format(self, record):
		if self.use_color and record.levelname in self.COLORS:
			if record.levelname in self.COLORS_ATTRS:
				record.msg = termcolor.colored(record.msg, self.COLORS[record.levelname], self.COLORS_ATTRS[record.levelname])
			else:
				record.msg = termcolor.colored(record.msg, self.COLORS[record.levelname])
		if threading.currentThread().getName() == 'MainThread':
			return self.mainthread_formatter.format(record)
		else:
			return logging.Formatter.format(self, record)

# }}}


if __name__ == '__main__':
	setup_logging()
	logging.info("Start")
	logging.debug("You touch my tralala?")

