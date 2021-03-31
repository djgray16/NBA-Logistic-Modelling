# -*- coding: utf-8 -*-
"""
Created on Sun Jan  3 18:09:01 2021

@author: djgra
"""
#kelly8(home,away,odds_home,odds_away,szn)
#kelly8("MIA","OKC",1.28,3.80,betszn)
#kelly8("HOU","DAL",1.85,1.95,betszn)
#kelly8("NOP","IND",1.80,2.00,betszn)

#betting rules
# once loss goes to 500
import timeit, time
#from datafinder import kelly8

#normalised SD is one half, and final bankroll is 2
#therefore STOP betting if you lose half the money
#invest 1000, STOP at 500
#no more models until validated on live data, not simulation
#demo wed



#kelly8(MIL,TOR,1.4,2.92)
#kelly8(LAL,BKN,1.78,2.16)


#test1 = game_leading_stats1(OKC,MIA,1,betszn)[0]
#test2 = game_leading_stats1(MIA,OKC,0,betszn)[1]
#test3 = game_leading_stats(OKC,MIA,1,betszn) 



#('HOU', '1.90', 'CHI', '2.00', '0.604', 'HOU', '0.0205', '1.90', 0.038907910500639215)
#0.5894269825653347

t=time.process_time()

kelly8(WAS,CHA,2.4,1.69)
kelly8(PHX,ATL,1.47,3.05)
kelly8(LAC,ORL,1.15,7.4)



elapsed = time.process_time() - t
print(elapsed, "time spent processing")

