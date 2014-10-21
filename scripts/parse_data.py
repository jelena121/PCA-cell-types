import numpy
import sys
import matplotlib
from numpy import linalg as LA
import matplotlib.pyplot as plt

columns= ''

with open(sys.argv[1]) as f: 
	content = f.readline()
	columns = content.split("\t")
	print columns

print len(columns)
	
# took out len(columns)
data = numpy.loadtxt(sys.argv[1], delimiter="\t", skiprows=2, usecols=range(1,10))

print data[1:10, 1:10]

covariance = numpy.cov(data)
print "hello"
w, v = LA.eigh(covariance)	
print covariance.shape

eigenpairs = zip(w, v)
eigenpairs.sort()
eigenpairs.reverse()

print eigenpairs

def pcaplot(dim1=0,dim2=1, outputfile=None):
	eig1 = eigenpairs[dim1][1]
	eig2 = eigenpairs[dim2][1]
	x = []
	y = []
	for i in range(0,data.shape[1]):
		x.append(numpy.dot(data[:,i], eig1))
		y.append(numpy.dot(data[:,i], eig2))
	print x
	print y
	plt.scatter(x, y)
	if (outputfile):
		plt.savefig(outputfile)
	else:
		plt.show()	
			
pcaplot(outputfile="plots/pcaplot.png")

