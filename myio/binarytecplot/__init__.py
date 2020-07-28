import struct
import sys

from   myio.binarytecplot.binary2asciifile                import *
from   myio.binarytecplot.tecplot.zone                    import *
from   myio.binarytecplot.tecplot.binary                  import *
from   myio.binarytecplot.tecplot.binary.filestructure    import *



def LoadTecplotFile(filename, mode = 'binary', info = False): 

	if   mode.lower() == 'binary': out =  FileStructure(filename)
	elif mode.lower() == 'ascii' : print("Cannot read ascii files at the moment."); sys.exit(-1) 
	else                         : print("Incorrect value of mode argument {}".format(mode))


	if info: print(out)

	return out



