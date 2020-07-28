import read_tecplot as reader
filename = 'OneraM6_SU2_RANS.dat'
zones, dfs, elements = reader.read_tecplot(filename, verbose=1)
print zones
print dfs
