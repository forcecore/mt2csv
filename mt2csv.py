#!/usr/bin/python3

import sys
import operator

class Mt2csv :
	def __init__( self ) :
		self.data = {}  # holds parsed data
			# data{ data_name } = array of values
		self.headers = [] # collect headers in order because dict has its own ordering.
		self.simulator = ""
		self.title = ""

	def read_tokens( self, f ) :
		result = []
		for line in f :
			toks = line.split()
			result.extend( toks )
		return result

	# modifies self.headers, self.data
	def parse_tokens( self, tokens ) :
		# fsm state description
		HEADER = 0
		VALUES = 1

		mode = HEADER
		header_len = 0
		i = 0
		for tok in tokens :
			# find '#'.
			if mode == HEADER :
				self.headers.append( tok )
				self.data[ tok ] = [] # allocate array
				if tok.find( '#' ) >= 0 :
					mode = VALUES
					header_len = len( self.headers )
			else : # VALUE mode
				head = self.headers[ i ]
				arr = self.data[ head ]
				arr.append( float( tok ) )
				i = (i+1) % header_len
				# print( head, tok )

	def read( self, fname ) :
		f = open( fname )
		self.simulator = f.readline().strip()
		self.title = f.readline().strip()

		tokens = self.read_tokens( f )
		self.parse_tokens( tokens )

	# func should be one of "max" or "min".
	def get_minmax( self, func, prefix ) :
		ns = []
		vals = []

		for (n, val) in self.data.items() :
			if n.startswith( prefix ) :
				vals.extend( val )
				ns.append( n )

		# by default, max is picked.
		if func == "min" :
			index, value = min( enumerate( vals ), key=operator.itemgetter(1) )
		else :
			index, value = max( enumerate( vals ), key=operator.itemgetter(1) )

		return ( ns[ index ], value )
	
	def get_avg( self, prefix ) :
		vals = []

		for (n, val) in self.data.items() :
			if n.startswith( prefix ) :
				vals.extend( val )

		return sum( vals ) / len( vals )
	
	def emit( self ) :
		print( self.simulator )
		print( self.title )

		# emit header
		print( ",".join( self.headers ) )

		# now for the data...
		# check data sanity
		data_len = -1
		for h in self.headers :
			arr = self.data[ h ]
			if data_len == -1 :
				data_len = len( arr )
			else :
				# print( data_len, len( arr ) )
				assert data_len == len( arr )

		# emit data, now!
		for i in range(0, data_len) :
			row = []
			for h in self.headers :
				arr = self.data[ h ]
				row.append( str( arr[ i ] ) )
			print( ",".join( row ) )



###
### main
###
if __name__ == "__main__" :
	fname = sys.argv[1]
	mt2csv = Mt2csv()
	mt2csv.read( fname )
	mt2csv.emit()
