import struct


class Binary2AsciiFile(object):
    """
    Binary2AsciiFile: 
        this class is a helpfull class to read a binary file characters. 
        Mainly, converts bytes to char, long integers, float, double, text
        
    Binary2AsciiFile(  filename )
    """
    def __init__(self, filename):
        """
        Arguments:
            ** filename = str() # the name of the binary file.
        """
        self.filename    = filename   
        try: 
            self.binaryfile  = open(filename,'rb')
        except IOError:
            print("file is open")			


    def _readLine    (self, size = 4): 
        """
            This is the Kernel of the class that read 
            some bytes from the file. 
            The default size is 4 bytes.

            ** size = int() # the number of bytes
        """
        return self.binaryfile.read(size)

    def _readChar           (self, size = 4):
        """
            This method reads a sequence of the bytes from 
            the file and converts to utf-8 format.
        """
        return self._readLine(size).decode("utf-8") 
    def _readLongInteger    (self):
        """
            read struct module for more information.
            This function reads a long integer.
        """
        return struct.unpack('l', self._readLine(4)) [0]
    def _readInteger        (self):
        """
            This function reads 4 bytes from the file and 
            convert to an integer. 
        """
        return struct.unpack('i', self._readLine(4)) [0]
    def _readFloat          (self):
        """
            This function reads 4 bytes from the file and 
            convert to a float number. 
        """       
        return struct.unpack('f', self._readLine(4)) [0]
    def _readDouble         (self):
        """
        This function reads 4 bytes from the file and 
        convert to a float number. 
        """       
        return struct.unpack('d', self._readLine(8)) [0]
    def _read_ListOfIntegers(self, n):
        return [self._readInteger() for _ in range(n)]

    def _Binary2Ascii       (self):
        """
            This method reads a string from a file. 
            The method continuously reads the file untile the null char 
            is read.
        """
        title = ""
        while True:
            ascii = self._readLine().decode('utf-8').replace(chr(0),"")
            if ascii=="": break
            title += ascii 

        return title



