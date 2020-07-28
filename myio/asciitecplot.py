# load tecplot ascii file following the format in the link
# from:  http://paulbourke.net/dataformats/tp/
#        -------------  ---------  ----------  ----------------------------------------------
#        Parameter      Ordered    Finite      Description
#                       Data       Element
#        -------------  ---------  ----------  ----------------------------------------------
#        T="title"      Yes        Yes         Zone title.
#        I=imax         Yes        No          Number of points in 1st dimension.
#        J=jmax         Yes        No          Number of points in 2nd dimension.
#        K=kmax         Yes        No          Number of points in 3rd dimension.
#        C=colour       Yes        Yes         Colour from WHITE, BLACK, RED, GREEN,
#                                                          BLUE, CYAN, YELLOW, PURPLE,
#                                                          CUST1, CUST2,....CUST8.
#        F=format       Yes        Yes         POINT or BLOCK for ordered data.
#                                              FEPOINT or FEBLOCK for finite element.
#        D=(list)       Yes        Yes         A list of variable names to to include
#                                              from the last zone.
#        DT=(list)      Yes        Yes         A list of datatypes for each variable.
#                                              SINGLE, DOUBLE, LONGINT, SHORTINT, BYTE, BIT.
#        N=num          No         Yes         Number of nodes.
#        E=num          No         Yes         Number of elements.
#        ET=type        No         Yes         Element type from TRIANGLE, BRICK,
#                                                                QUADRILATERAL, TETRAHEDRON.
#        NV=variable    No         Yes         Variable for node value.
#        -------------  ---------  ----------  ----------------------------------------------
# principle: to make the reading as liberal as possible
# developer: @ Yu Lv, yl723@msstate.edu
# limitation: 1) tecplot text section not supported
#             2) currently support single zone
#             3) fe data only support hex and tet

import numpy as np

nodes_per_elem = {'FETRIANGLE':3, 'FEQUADILATERAL':4, 'FETETRAHEDRON':4, 'FEBRICK':8}

def split_line(line):
    """splits a comma or space separated line"""
    if ',' in line:
        line2 = line.replace(',', ' ')
        sline = line2.split()
    else:
        sline = line.split()
    return sline

def is_number(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

def read_tecplot_ascii(filename): 
    
    fp = open(filename)
    
    merge = [] 
    
    # collect header info
    for i in range(50):
        
        line = fp.readline()
        
        # stop criterion
        line = line.replace("\n", " ")
        line = line.replace(",",  " ")
        #line = line.replace("\"", " ") 
        entry = line.split(" ")
        entry = list(filter(None, entry))
        if len(entry) >= 2:
            if is_number(entry[0]) and is_number(entry[1]):
                break
        
        merge = merge + entry
     
    header = []
    for idx in range(len(merge)):
        if '=' in merge[idx]:
            entry = merge[idx].split("=")
            entry = list(filter(None, entry))
            header.extend(entry) 
        else:
            header.append(merge[idx])
    
    for item in header: 
        if item == '\"':
            header.remove('\"')
    
    # search key words
    for idx in range(len(header)):
        item = header[idx]
        # "variables"
        if item == 'Variable' or item == 'variable' or item == 'Variables' \
            or item == 'variables' or item == 'VARIABLE' or item == 'VARIABLES':
            var_index = idx
    
        # "zone"
        if item == 'zone' or item == 'Zone' or item == 'ZONE':
            zone_index = idx
    
    
    varlist_org = header[var_index+1:zone_index]
    varlist = []
    # if space included in varname, correction needed
    space_contained = False
    for item in varlist_org:
        if item.count('\"') == 0:
            if space_contained:
                varlist[-1] = varlist[-1] + ' ' + item
            else:
                varlist.append(item)
        elif item.count('\"') == 2:
            varlist.append(item[1:-1]) # remove quotes
        elif item.count('\"') == 1:
            if item[0] == '\"':
                varlist.append(item[1:])
                space_contained = True
            if item[-1] == '\"':
                varlist[-1] = varlist[-1] + ' ' + item[:-1]
                space_contained = False
        else:
            print('no other case')
    
    
    zone    = header[zone_index+1:]
    
    # get format
    zonetype = 'FEM'
    for item in zone:
        if 'point' == item.lower():
            formt = 'POINT'
        
        if 'block' == item.lower():
            formt = 'BLOCK'
        
        if 'i' == item.lower():
            zonetype = 'ORDERED'
    
    if zonetype == 'ORDERED':
    
        if 'i' in zone:
            num_i = int(zone[zone.index('i')+1])
        elif 'I' in zone:
            num_i = int(zone[zone.index('I')+1])
        else:
            print('no. index i provided')
    
        if 'j' in zone:
            num_j = int(zone[zone.index('j')+1])
        elif 'J' in zone:
            num_j = int(zone[zone.index('J')+1])
        else:
            print('no. index j provided')
        
        if 'k' in zone:
            num_k = int(zone[zone.index('k')+1])
        elif 'K' in zone:
            num_k = int(zone[zone.index('K')+1])
        else:
            print('no. index k provided')
    
        # allocate memory
        nnode  = num_i * num_j * num_k
        nvar   = len(varlist) - 3
        xyz    = np.zeros((nnode, 3),    dtype='float32')
        result = np.zeros((nnode, nvar), dtype='float32')
        elemlist = None
        elementtype = None
        dims   = (num_i, num_j, num_k)

        if formt == 'POINT':
            sline = split_line(line)
            for idx in range(3):
                xyz[0, idx] = float(sline[idx])
        
            for idx in range(nvar):
                result[0, idx] = float(sline[idx+3])
            
            for iline in range(1, nnode):
                line = fp.readline()
                sline = split_line(line)
        
                for idx in range(3):
                    xyz[iline, idx] = float(sline[idx])
                for idx in range(nvar):
                    result[iline, idx] = float(sline[idx+3])
        elif formt == 'BLOCK':
            sline = split_line(line)
            iline = 0
            for item in sline:
                xyz[iline, 0] = float(item)
                iline = iline + 1
            
            # coordinate
            for idx in range(3):
                while True:
                    line = fp.readline()
                    sline = split_line(line)
                    
                    for item in sline:
                        xyz[iline, idx] = float(item)
                        iline = iline + 1
                        
                    if iline == nnode:
                        break
                # for next component 
                iline = 0
            
            # result
            for idx in range(nvar):
                while True:
                    line = fp.readline()
                    sline = split_line(line)
        
                    for item in sline:
                        result[iline, idx] = float(item)
                        iline = iline + 1
        
                    if iline == nnode:
                        break
                # for next component
                iline = 0
        else:
            pass
    
    #if formt == 'FEPOINT' or formt == 'FEBLOCK':
    else:
        # if not the previous case, then process FEM data
        if 'nodes' in zone:
            nnode = int(zone[zone.index('nodes')+1])
        elif 'Nodes' in zone:
            nnode = int(zone[zone.index('Nodes')+1])
        elif 'NODES' in zone:
            nnode = int(zone[zone.index('NODES')+1])
        else:
            print('no. num of nodes provided')
       
        if 'elements' in zone:
            nelem = int(zone[zone.index('elements')+1])
        elif 'Elements' in zone:
            nelem = int(zone[zone.index('Elements')+1])
        elif 'ELEMENTS' in zone:
            nelem = int(zone[zone.index('ELEMENTS')+1])
        else:
            print('no. num of elements provided')
     
        # find element type 
        for item in zone:
            if 'fe' in item or 'FE' in item:
                elementtype = item.upper()
    
        # may be improved in the next release
        if elementtype == 'FETRIANGLE' or elementtype == 'FEQUADRILATERAL':
            print('only support 3D element')  
    
        nvar   = len(varlist) - 3
        xyz    = np.zeros((nnode, 3),    dtype='float32')
        result = np.zeros((nnode, nvar), dtype='float32')
        nnodesperelement = nodes_per_elem[elementtype]
        elemlist = np.zeros((nelem, nnodesperelement), dtype='int')
        dims   = None

        if formt == 'POINT':
            sline = split_line(line)
            for idx in range(3):
                xyz[0, idx] = float(sline[idx])
        
            for idx in range(nvar):
                result[0, idx] = float(sline[idx+3])
            
            for iline in range(1, nnode):
                line = fp.readline()
                sline = split_line(line)
        
                for idx in range(3):
                    xyz[iline, idx] = float(sline[idx])
                for idx in range(nvar):
                    result[iline, idx] = float(sline[idx+3])
            
        if formt == 'BLOCK':
            sline = split_line(line)
            iline = 0
            for item in sline:
                xyz[iline, 0] = float(item)
                iline = iline + 1
    
            # coordinate
            for idx in range(3):
                while True:
                    line = fp.readline()
                    sline = split_line(line)
                    
                    for item in sline:
                        xyz[iline, idx] = float(item)
                        iline = iline + 1
                        
                    if iline == nnode:
                        break
                # for next component 
                iline = 0
            
            # result
            for idx in range(nvar):
                while True:
                    line = fp.readline()
                    sline = split_line(line)
        
                    for item in sline:
                        result[iline, idx] = float(item)
                        iline = iline + 1
        
                    if iline == nnode:
                        break
                # for next component
                iline = 0
    
        # skip empty line
        while True:
            line = fp.readline()
            sline = split_line(line)
        
            if len(sline) != 0:
                break
        
        # load element connectivity; offset=-1 to consistent with VTK
        for idx in range(nnodesperelement):
            elemlist[0, idx] = int(sline[idx])-1
        
        for iline in range(1, nelem):
            line = fp.readline()
            sline = split_line(line)
            
            for idx in range(nnodesperelement):
                elemlist[iline, idx] = int(sline[idx])-1

    fp.close()

    return varlist, xyz, result, elemlist, elementtype, dims


#filepath = 'test_tec.dat'
#filepath = 'test_tec_block.dat'
#filepath = 'unstr_sample.dat'
#filepath = 'unstr_sample_block.dat'
#varlist, xyz, result, elemlist, elemtype, dims, = read_tecplot_ascii(filepath)
#print(elemlist)

class tecdata(object):
    
    variables   = None
    xyz         = None
    results     = None
    elements    = None
    elementtype = None
    dims        = None

    def __init__(self):
        pass

    def read_tecplot(self, filename):
        self.variables, self.xyz, self.results, self.elements, self.elementtype, self.dims = \
                read_tecplot_ascii(filename)

