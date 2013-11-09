#!/usr/bin/python -O
# -*- coding: iso-8859-1 -*-

class CRC64(): # {{{
	# Initialisation
	# 32 first bits of generator polynomial for CRC64
	# the 32 lower bits are assumed to be zero

	POLY64REVh = 0xd8000000L
	the_string = None
	the_crc = None
	CRCTableh = None
	CRCTablel = None

	def __init__(self, ):
		pass

	# only init if necessary
	def init(self,):
		if self.CRCTableh is None:
			self.CRCTableh = [0] * 256
			self.CRCTablel = [0] * 256
			for i in xrange(256):
				partl = i
				parth = 0L
				for j in xrange(8):
					rflag = partl & 1L
					partl >>= 1L
					if (parth & 1):
						partl |= (1L << 31L)
					parth >>= 1L
					if rflag:
						parth ^= self.POLY64REVh
				self.CRCTableh[i] = parth;
				self.CRCTablel[i] = partl;


	def crc(self, aString=None):
		if aString is not None:
			self.the_string = aString
			self.the_crc = None
		if not self.the_string:
			return None
		if not self.the_crc:
			self.init()
			crcl = 0
			crch = 0
			for item in self.the_string:
				shr = 0L
				shr = (crch & 0xFF) << 24
				temp1h = crch >> 8L
				temp1l = (crcl >> 8L) | shr
				tableindex = (crcl ^ ord(item)) & 0xFF

				crch = temp1h ^ self.CRCTableh[tableindex]
				crcl = temp1l ^ self.CRCTablel[tableindex]
			self.the_crc = (crch, crcl)
		return self.the_crc

	def digest(self, aString=None):
		self.crc(aString)
		return "%08X%08X" % self.the_crc

	def bigint(self, aString=None):
		try:
			return int(self.digest(aString), 16)
		except TypeError: # in case of 'None'
			return 0

# }}}

if __name__ == '__main__':
	print CRC64().crc('')
	print CRC64().bigint("a la volette")

