#coding: UTF8
"""
Prints out a table, padded to make it pretty.

call pprint_table with an output (e.g. sys.stdout, cStringIO, file)
and table as a list of lists. Make sure table is "rectangular" -- each
row has the same number of columns.

2013/10/08, Kyle Boone:
Update to work with python3
Added pprint_list as an easy way to print lists since it seems like I use this
module for that a lot.

2010/12/16, Kyle Boone:
Found this at: http://ginstrom.com/scribbles/2007/09/04/pretty-printing-a-table-in-python/
Modified the file to add borders for SQL style prettiness

MIT License
"""

__version__ = "0.1"
__author__ = "Ryan Ginstrom"

import locale
import sys
locale.setlocale(locale.LC_NUMERIC, "")

def format_num(num):
	"""Format a number according to given places.
	Adds commas, etc.
	
	Will truncate floats into ints!"""

	try:
		inum = int(num)
		return locale.format("%.*f", (0, inum), True)

	except (ValueError, TypeError):
		return str(num)

def get_max_width(table, index):
	"""Get the maximum width of the given column index
	"""
	
	return max([len(format_num(row[index])) for row in table])

def pprint_table(out, table):
	"""Prints out a table of data, padded for alignment
	
	@param out: Output stream ("file-like object")
	@param table: The table to print. A list of lists. Each row must have the same
	number of columns.
	
	"""

	col_paddings = []
	
	for i in range(len(table[0])):
		col_paddings.append(get_max_width(table, i))
	
	# print a bar across the top
	tableWidth = sum(col_paddings) + 1 + len(table[0]) * 3
	print('+' + '-'*(tableWidth-2) + '+', file=out)

	for row in table:
		# left col
		print('|', format_num(row[0]).ljust(col_paddings[0]), '|',
                        file=out, end="")
		# rest of the cols
		for i in range(1, len(row)):
			col = format_num(row[i]).ljust(col_paddings[i])
			print(' ' + col, '|', file=out, end="")
		print(file=out)
		
		# after the first line, print another bar across
		if row == table[0]:
			print('+' + '-'*(tableWidth-2) + '+', file=out)

	# bar for the bottom
	print('+' + '-'*(tableWidth-2) + '+', file=out)

if __name__ == "__main__":
	table = [["", "taste", "land speed", "life"],
		["spam", 300101, 4, 1003],
		["eggs", 105, 13, 42],
		["lumberjacks", 13, 105, 10]]
	
	import sys
	out = sys.stdout
	pprint_table(out, table)

def pprint_list(items, title):
    """Print a table of items. An index will be printed in one column and the
    items' __str__ representations in the other."""
    pprint_table(sys.stdout, [('Id', title)] + [(i, items[i]) for i in
        range(len(items))])
