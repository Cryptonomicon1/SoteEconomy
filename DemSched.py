import pandas as pd
from random import random
from random import randint
import time

#Load Goods List
goods_list = pd.read_csv(r'Production Schedule.csv')
goods_list = goods_list['goods'].to_list()

goods_cnt = {}		#goods count
goods_prcs = {}		#goods prices
'''
#Make Goods Stockpile
for i in range( len( goods_list ) ):
	if i % 2 == 0:
		goods_cnt[ goods_list[i] ] = 10000
	else:
		goods_cnt[ goods_list[i] ] = 2

#Goods Prices (random for now)
for i in range( len( goods_list ) ):
	goods_prcs[ goods_list[i] ] = 4 * random() + 1
	
#del goods_list
'''
#Load Demand List
dmnd_list = pd.read_csv(r'Demand Schedule.csv')

def buyGoods( income ):
	i = 0
	luxury_marker = 0
	while income > 0:
		
		#print( 'i= ', i )
		
		#Set marker right after luxury needs tag to loop over luxury needs
		if luxury_marker == 0 and dmnd_list[ 'good' ][ i ] == 'luxury needs':
			i += 1
			luxury_marker = i
		
		#After this, we know that the rest of the if-else block the i is not out of bounds.
		elif i >= len( dmnd_list ):
			i = luxury_marker
		
		#Skip demand schedule section tags
		elif dmnd_list[ 'good' ][ i ] == 'subsistence needs' or dmnd_list[ 'good' ][ i ] == 'basic needs':
			i += 1
			
		elif 100 != int( dmnd_list[ 'preference' ][ i ] ):
			desired = ( float( dmnd_list[ 'amount' ][ i ] ) + float( dmnd_list[ 'amount' ][ i+1 ] ) ) / 2
			available = goods_cnt[ dmnd_list[ 'good' ][ i ] ] + goods_cnt[ dmnd_list[ 'good' ][ i+1 ] ]
			total_bought = min( desired, available )
			
			price1 = goods_prcs[ dmnd_list[ 'good' ][ i ] ]
			price2 = goods_prcs[ dmnd_list[ 'good' ][ i+1 ] ]
			
			#Kind of inversion or parallel circuit equation for 2 resistors.
			#Higher price = lower desire to buy it.
			price_ratio1 = price2 / ( price1 + price2 )
			price_ratio2 = price1 / ( price1 + price2 )
			
			pref1 = float( dmnd_list[ 'preference' ][ i ] ) / 100
			pref2 = float( dmnd_list[ 'preference' ][ i+1 ] ) / 100
			bought1 = total_bought * ( ( price_ratio1 + pref1 ) / 2 )
			bought2 = total_bought * ( ( price_ratio2 + pref2 ) / 2 )
			
			#If remaining income cannot buy total goods, then ratio down by remaining income.
			income_ratio = min( 1, income / ( bought1 * price1 + bought2 * price2 ) )
			bought1 *= income_ratio
			bought2 *= income_ratio
			
			#We already found the minimum of the total available and total desired.
			#However, we will need the minimum of each available and each desired.
			#Then, we can ensure that we won't overbuy. When we scale one good down
			#to a lower level supply in stock, then we need to ensure that we don't
			#overspend our income. So, we need to only scale the good that is not
			#limited by stock up to the minimum of the total desired goods and our
			#total income.
			
			if goods_cnt[ dmnd_list[ 'good' ][ i ] ] < bought1:
				#Floating Point Errors cause the algo to sometimes bring stocks < 0. Then bad things happen.
				in_stock1 = max( 0, goods_cnt[ dmnd_list[ 'good' ][ i ] ] )
				income_diff = income - ( in_stock1 * price1 + bought2 * price2 )
				bought2_addr = min( bought1 - in_stock1, income_diff / price2 )
				bought1 = in_stock1
				bought2 += bought2_addr
			elif goods_cnt[ dmnd_list[ 'good' ][ i+1 ] ] < bought2:
				#Floating Point Errors cause the algo to sometimes bring stocks < 0. Then bad things happen.
				in_stock2 = max( 0, goods_cnt[ dmnd_list[ 'good' ][ i+1 ] ] )
				income_diff = income - ( bought1 * price1 + in_stock2 * price2 )
				bought1_addr = min( bought2 - in_stock2, income_diff / price1 )
				bought1 += bought1_addr
				bought2 = in_stock2
			
			income -= bought1 * price1 + bought2 * price2
			goods_cnt[ dmnd_list[ 'good' ][ i ] ] -= bought1
			goods_cnt[ dmnd_list[ 'good' ][ i+1 ] ] -= bought2
			
			#print('Good1: ', dmnd_list[ 'good' ][ i ], '  In Stock: ', goods_cnt[ dmnd_list[ 'good' ][ i ] ], '  Price1: ', price1, '  Bought: ', bought1, '  Income: ', income )
			#print('Good2: ', dmnd_list[ 'good' ][ i+1 ], '  In Stock: ', goods_cnt[ dmnd_list[ 'good' ][ i+1 ] ], '  Price2: ', price2, '  Bought: ', bought2, '  Income: ', income )
			#print(' ')
			#time.sleep(1)
			i += 2
		else:
			#Good with no substitute: Either buy with last of budget/income or buy the last in stock
			price = goods_prcs[ dmnd_list[ 'good' ][ i ] ]
			
			bought = min( goods_cnt[ dmnd_list[ 'good' ][ i ] ], float( dmnd_list[ 'amount' ][ i ] ) )
			bought = min( bought, income / price )
			
			goods_cnt[ dmnd_list[ 'good' ][ i ] ] -= bought
			income -= bought * price
			
			#print('Good: ', dmnd_list[ 'good' ][ i ], '  In Stock: ', goods_cnt[ dmnd_list[ 'good' ][ i ] ],  '  Price: ', price, '  Bought: ', bought, '  Income: ', income )
			#print(' ')
			#time.sleep(1)
			i += 1

times = []
for i in range(1000):
	income = randint(1000, 2000)
	
	#Set/Reset goods stockpile amounts
	for j in range( len( goods_list ) ):
		if j % 2 == 0:
			goods_cnt[ goods_list[j] ] = 10000
		else:
			goods_cnt[ goods_list[j] ] = 2
	
	#Set/Reset goods prices
	for j in range( len( goods_list ) ):
		goods_prcs[ goods_list[j] ] = 4 * random() + 1
	
	t1 = 1000 * time.time()
	buyGoods(income)
	t2 = 1000 * time.time()
	times.append( t2 - t1 )

print( 'Average Time:', round( sum( times ) / len( times ), 2 ), 'milliseconds' )
	