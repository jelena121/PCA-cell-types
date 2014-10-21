# takes in the matrix of processed data as 1st argument
# metadata file as 2nd argument
# plots a pca plot

import numpy
import sys
import matplotlib
from numpy import linalg as LA
import matplotlib.pyplot as plt
import matplotlib.cm as cm

columns= ''
factormap = {}
factorlist = {}

# metadata reading in
with open(sys.argv[2]) as f:
	f.readline() 
	while True:
		line = f.readline()
		line.strip()
		if len(line) == 0:
			break
		tmp = line.split("\t")
		factormap[tmp[0]] = tmp[32]
		factorlist[tmp[32]] = True


with open(sys.argv[1]) as f: 
	content = f.readline()
	columns = content.split("\t")
	del columns[0]

print "Reading in data matrix"
data = numpy.loadtxt(sys.argv[1], delimiter="\t", skiprows=2, usecols=range(1,len(columns)))

covariance = numpy.cov(data)

print "Calculating Eigenvectors"
w, v = LA.eigh(covariance)	

print "Saving Eigenvectors to file"
numpy.savetxt(w, "eigenweights.tsv")
numpy.savetxt(v, "eigenvectors.tsv")

eigenpairs = zip(w, v)
eigenpairs.sort()
eigenpairs.reverse()

print eigenpairs

def pcaplot(dim1=0,dim2=1, outputfile=None):
	eig1 = eigenpairs[dim1][1]
	eig2 = eigenpairs[dim2][1]
	colors = iter(cm.rainbow(numpy.linspace(0, 1, len(factorlist.keys()))))
	plt.figure()
	for factorname in factorlist.keys():
		x = []
		y = []
		for i in range(0, data.shape[1]):
			columnname = columns[i].strip("\"")
			if factormap[columnname] != factorname:
				continue
			
			
			x.append(numpy.dot(data[:,i], eig1))
			y.append(numpy.dot(data[:,i], eig2))
		print x
		print y
		plt.scatter(x, y, label=factorname, color=next(colors))
	plt.legend()
	if (outputfile):
		plt.savefig(outputfile)
	else:
		plt.show()	
			
print "Working on PCA plots"
pcaplot(outputfile="plots/pcaplot_1st_2nd.png")

pcaplot(dim1=1, dim2=2, outputfile="plots/pcaplot_2nd_3rd.png")

