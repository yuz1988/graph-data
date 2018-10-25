import numpy, scipy.io

arr = numpy.arange(9)
arr = arr.reshape((3, 3))
scipy.io.savemat('test.mat', mdict={'arr': arr})