#!/usr/bin/python3

import sys

class Mt2csv :
	data = {}  # holds parsed data
		# data{ data_name } = array of values
	headers = [] # collect headers in order because dict has its own ordering.
	simulator = ""
	title = ""

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
				arr.append( tok )
				i = (i+1) % header_len
				# print( head, tok )

	def read( self, fname ) :
		f = open( fname )
		self.simulator = f.readline().strip()
		self.title = f.readline().strip()

		tokens = self.read_tokens( f )
		self.parse_tokens( tokens )
	
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
				row.append( arr[ i ] )
			print( ",".join( row ) )



###
### main
###
if __name__ == "__main__" :
	fname = sys.argv[1]
	mt2csv = Mt2csv()
	mt2csv.read( fname )
	mt2csv.emit()
