from matplotlib import pyplot as plt
import numpy as np
import math

peak = 10
sigma = peak / 3
mult = sigma / ( peak * 12 )
#x_shift = -0.00001
y_shift = ( sigma * 2.71828 ** (1/2) ) / peak

m = 1000

def firmFunc( x, s, p ):
	out = np.arange(0)
	lim1 = p / ( 2.71828 ** (1/2) )
	flat = ( s * 2.71828 ** (1/2) ) / p
	
	for i in range( len( x ) ):
		if x[i] <= 0:
			out = np.append( out, 0 )
		
		elif x[i] <= lim1:
			out = np.append( out, flat )
		
		else:
			out = np.append( out, s / ( x[i] * ( -2 * math.log( x[i] / p ) )**(1/2) ) )
	
	return out

q = np.arange(0, peak - 0.0001, peak / 100)
mh1 = firmFunc( q, sigma, peak )

mh2 = np.arange(0)
for i in range( len( q ) ):
	#print( mult / ( math.log( peak ) - math.log( q[i] - shift ) ) )
	if q[i] <= 0:
		mh2 = np.append( mh2, 0 )
	else:
		mh2 = np.append( mh2, mult / ( math.log( peak ) - math.log( q[i] ) ) + y_shift )

fig = plt.figure()
axes = fig.add_axes([ 0.1, 0.1, 0.8, 0.8 ])

axes.plot(q, mh1)
axes.plot(q, mh2)
#axes.xlabel("Quantity")
#axes.ylabel("Man-Hours")
#axes.title("Firm Curve Equivalent")

#axes.set_ylim([ 0, 4 ])

plt.show()