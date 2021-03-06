
import numpy as np


__ORDERED__               = 0
__FELINESEG__             = 1
__FETRIANGLE__            = 2
__FEQUADRILATERAL__       = 3
__FETETRAHEDRON__         = 4
__FEBRICK__               = 5
__FEPOLYGON__             = 6
__FEPOLYHEDRON__          = 7


__NO_SHARE_CONNECTIVITY__ = -1


__TEC_FLOAT__    =   1
__TEC_DOUBLE__   =   2
__TEC_LONG_INT__ =   3
__TEC_INT__      =   4


class Zone(object):
    """docstring for Zone"""
    def __init__(self):


        self.name                    = ""
        self.variable                = [] # copied from filestructure file
        self.parent_zone             = int()
        self.strand_id               = int()
        self.solutiontime            = float() # double precision 8 bytes
        self.not_used                = int()

        self.variable_format         = []
        self.passive_variables       = []
        self.variable_sharing        = []

        self.ShareConnectivity       = int() # if -1 no sharing
        self.connectivity            = [] #double list eadh element is []
        self.min_value               = []
        self.max_value               = []
        self.data                    = [] #double list eadh element is the data the viariable
        # <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
        # Zone Type
        #
        # 0 = ORDERED       1 = FELINESEG 2 = FETRIANGLE 3 = FEQUADRILATERAL
    # 4 = FETETRAHEDRON 5 = FEBRICK   6 = FEPOLYGON  7 = FEPOLYHEDRON
    #
        # <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
        self.type          = int()
        # <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
        # Data Packing
        #
        # 0 = BLOCK
        # 1 = POINT
        # <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
        self.datapacking      = int()

        # <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
        # Zones
        # <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>

        self.var_location     = int() # if varlocation    is not equal to zero you must do more stuff ...
        self.face_neighbors   = int() # if face_neighbors is not equal to zero you must do more stuff ...

        self.number_elements  = int()
        self.number_points    = int()
        # <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
        # ORDERED ZONE
        # <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
        self.imax = int()
        self.jmax = int()
        self.kmax = int()
        # <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
        # FINITE ELEMENT ZONE
        # <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
        self.icell = int()
        self.jcell = int()
        self.kcell = int()

    def _ReadZoneVars                 (self,rInt,rFloat,rDouble,rAscii    ):
        self.name        = rAscii ()
        self.parentzone  = rInt   ()
        self.strand_id   = rInt   ()
        self.solutiontime= rDouble()
        self.not_used    = rInt   ()
        self.type        = rInt   ()
        #self.datapacking = rInt   ()
        self.var_location= rInt   () # if varlocation    is not equal to zero you must do more stuff ...

        assert self.var_location   == 0
        
        self.face_neighbors   = rInt() # if face_neighbors is not equal to zero you must do more stuff ...

        assert self.face_neighbors == 0

        dummy = rInt ()

        if    self.type == __ORDERED__         : self.OrderedZone(rInt,rFloat,rDouble,rAscii)
        if    self.type == __FELINESEG__       \
          or  self.type == __FETRIANGLE__      \
          or  self.type == __FEQUADRILATERAL__ \
          or  self.type == __FETETRAHEDRON__   \
          or  self.type == __FEBRICK__         \
          or  self.type == __FEPOLYGON__       \
          or  self.type == __FEPOLYHEDRON__    : 
              print('here')
              self.FiniteElementZone(rInt,rFloat,rDouble,rAscii)
    def OrderedZone                   (self,rInt,rFloat,rDouble,rAscii    ):

        self.imax = rInt ()
        self.jmax = rInt ()
        self.kmax = rInt ()

        if   self.jmax == 1 and self.kmax == 1 : self.number_elements = (self.imax -1) # 1D data
        elif self.kmax == 1                    : self.number_elements = (self.imax -1) * (self.jmax -1)
        else                                   : self.number_elements = (self.imax -1) * (self.jmax -1) * (self.kmax-1)

        self.number_points = self.imax * self.jmax * self.kmax
    def FiniteElementZone             (self,rInt,rFloat,rDouble,rAscii    ):
        self.number_points = rInt ()

        
        zt = self.type
        if zt == __FEPOLYGON__ or zt == __FEPOLYHEDRON__:
            self.number_faces              = rInt ()
            self.total_faces               = rInt ()
            self.boundary_faces            = rInt ()
            self.total_boundary_connections= rInt ()


        self.number_elements = rInt()
        self.icell           = rInt() # for future usage, set to zero
        self.jcell           = rInt() # for future usage, set to zero
        self.kcell           = rInt() # for future usage, set to zero

    def ReadZoneData                  (self, ReadFunction                 ):
        if    self.var_location != 0: print("DEVELOP THIS CASE") # self.vars_location do not exist
        return [ReadFunction() for _ in range(self.number_points) ]
    def set_ShareConnectivity         (self, val                          ): self.ShareConnectivity = val
    def Read_MinMaxOfValues           (self,NumberOfVariables,ReadFunction):

        for _ in range(NumberOfVariables):
            self.min_value.append( ReadFunction() )
            self.max_value.append( ReadFunction() )
    def ChooseProperFunctionToReadData(self,         variable , rFloat, rDouble, rLongInt, rInt):
        """
        This function returns a proper function based on the format of the
        variable to read the corresponding data from the file.

        if passive_variables[var] == 1 -> float
        if passive_variables[var] == 2 -> double
        if passive_variables[var] == 3 -> Long Integer
        if passive_variables[var] == 4 -> Integer

        """

        vfmt = self.variable_format[variable]

        if   vfmt == __TEC_FLOAT__   : return rFloat
        elif vfmt == __TEC_DOUBLE__  : return rDouble
        elif vfmt == __TEC_LONG_INT__: return rLongInt
        elif vfmt == __TEC_INT__     : return rInt
        else                                      : print("type of data not supported: {}".format(vfmt)); sys.exit(1)
    def Read_DataTables               (self, NumberOfVariables, rFloat, rDouble, rLongInt, rInt):
        print(NumberOfVariables)
        for var in range(NumberOfVariables):

            if not self.passive_variables[var]:

                ReadFunction = self.ChooseProperFunctionToReadData(
                        var,
                        rFloat      ,
                        rDouble     ,
                        rLongInt    ,
                        rInt)

                self.data.append( self.ReadZoneData( ReadFunction  ) )
    def ConnectivityExists            (self): return self.ShareConnectivity == __NO_SHARE_CONNECTIVITY__
    def isFiniteElementZone           (self):

        return \
        self.type == __FELINESEG__       or \
        self.type == __FETRIANGLE__      or \
        self.type == __FEQUADRILATERAL__ or \
        self.type == __FETETRAHEDRON__   or \
        self.type == __FEBRICK__         or \
        self.type == __FEPOLYGON__       or \
        self.type == __FEPOLYHEDRON__
    def getNodesPerElement            (self):
        if   self.type == __FELINESEG__       : return 2
        elif self.type == __FETRIANGLE__      : return 3
        elif self.type == __FEQUADRILATERAL__ : return 4
        elif self.type == __FETETRAHEDRON__   : return 4
        elif self.type == __FEBRICK__         : return 8
    def Read_FiniteElements           (self, rListInt):
        for _ in range(self.number_elements):
            element = rListInt( n = self.getNodesPerElement() )
            self.connectivity.append(element)

    # <><><><><><><><><><><><><><><><><><><><><><><><>
    #
    # GETTERS
    #
    # <><><><><><><><><><><><><><><><><><><><><><><><>
    def getName            (self)          : return self.name
    def getParentZone      (self)          : return self.parent_zone
    def getStrand_id       (self)          : return self.strand_id
    def getSolutionTime    (self)          : return self.solutiontime
    def getVariableFormat  (self)          : return self.variable_format
    def getPassiveVariables(self)          : return self.passive_variables
    def getVariableSharing (self)          : return self.variable_sharing
    def getConnectivity    (self)          : return np.array(self.connectivity)
    def getVariable        (self, var_id)  : return self.variable[var_id]
    def getData            (self, var_id)  : return np.array(self.data[var_id]).astype(np.float64)
    def getDataType        (self)          : return self.type
    def getDataPacking     (self)          : return self.datapacking
    def getNumberOfPoints  (self)          : return self.number_points
    def getNumberOfElements(self)          : return self.number_elements
    def __getitem__        (self, var_name): return self.getData( self.variable.index(var_name) )

    def __repr__ (self):
        line = ""
        commit = "    Zone Name           : {} \n".format(self.name           ) ; line += commit
        commit = "    Parent Zone         : {} \n".format(self.parent_zone    ) ; line += commit
        commit = "    Strand Id           : {} \n".format(self.strand_id      ) ; line += commit
        commit = "    Solution Time       : {} \n".format(self.solutiontime   ) ; line += commit
        commit = "    Finite Element Type : {} \n".format(self.type           ) ; line += commit
        commit = "    Data Packing        : {} \n".format(self.datapacking    ) ; line += commit
        commit = "    Number of Points    : {} \n".format(self.number_points  ) ; line += commit
        commit = "    Number of Elements  : {} \n".format(self.number_elements) ; line += commit

        return line
