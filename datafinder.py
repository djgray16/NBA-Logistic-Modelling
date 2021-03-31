# -*- coding: utf-8 -*-
"""
Created on Thu Nov 26 14:31:20 2020

@author: djgra
"""

#from nba_api.stats.static import players

from nba_api.stats.static import teams 
teams = teams.get_teams()
import pandas as pd
import random 
import time
from nba_api.stats.endpoints import scoreboardv2,boxscoreadvancedv2,leaguedashteamptshot,leaguedashoppptshot,teamdashboardbyyearoveryear,teamdashboardbyteamperformance,teamestimatedmetrics,teamdashboardbyopponent
import numpy as np
import math
from scipy.stats import norm
from datetime import date
from Scrape_NBA_injuries import injuries

#coefficients = [(Intercept),locationGame.team1.H,net_rtg.team2
#,net_rtg.team1,winpct.team1,winpct.team2,ptsTeam.own.agg.per100.team1 \
                #ptsTeam.own.agg.per100.team2,stlTeam.own.agg.per100.team1,
 #               blkTeam.own.agg.per100.team2,fgpct.own.agg.team2,fgpct.own.agg.team1,\
                #fg2pct.own.agg.team2,fg2pct.own.agg.team1,fg2pct.opp.agg.team2,
  #              fgmTeam.own.agg.per100.team1,astTeam.opp.agg.per100.team2,
   #             fgmTeam.own.agg.per100.team2,fgpct.opp.agg.team1,fg2pct.opp.agg.team1,
   #             fgpct.opp.agg.team2\]
   
def sanity_check(nothing):
    game_stats = game_leading_stats("TOR","NOP",1,testszn) # this uses old_old_coeff
    if winprob(game_stats) == 0.7871644479795692: #0.7863433056912315:
        print("Model still working")
    else:
        print("Error somewhere")
    return ("idk")

coeff = np.array([0.3254408,-0.8441886,0.0958306,-0.0487357,-1.0344844,0.4628635,-0.0135695,0.0005196,-0.0375902,0.0251853,-2.0985794,3.5077161,4.2236479,
                  -4.0172592,-6.3779728,0.0114720,-0.0144738,-0.0448563,-6.0072478,7.4125775,11.1549654]) # includes 2020
old_coeff = np.array([0.725662,-0.839862,0.095545 ,-0.050152,-0.97344,0.333520,-0.018394,0.007666,-0.053650,0.012082,-1.901349,2.535272,3.888329,-3.269429,
                  -7.849940,0.017334,-0.016553,-0.044861,-7.032992,8.350849,11.747888])  # coefficients when the model had the right correct sf but not 2020
old_old_coeff = np.array([0.835126  , -0.839524,0.100908,-0.049996,
                  -0.971874, 0.165552,-0.018518,  0.007933,
                  -0.054079, 0.011759, -1.891725, 2.544475,
                  3.917097, -3.281942, -7.931972,0.017015,
                  -0.015570,-0.046170, -7.067879,  8.395788,
                  11.798384]) 
    
    
    
"""                (Intercept)         locationGame.team1.H                net_rtg.team2                net_rtg.team1 
                 0.811768822                 -0.811568929                  0.081412060                 -0.058456117 
                winpct.team1                 winpct.team2 ptsTeam.own.agg.per100.team1 ptsTeam.own.agg.per100.team2 
                -0.902194210                  0.293921414                 -0.016987588                  0.028936479 
stlTeam.own.agg.per100.team1 blkTeam.own.agg.per100.team2          fgpct.own.agg.team2          fgpct.own.agg.team1 
                -0.032569790                  0.006970042                 -0.218255603                 -0.200022118 
        fg2pct.own.agg.team2         fg2pct.own.agg.team1         fg2pct.opp.agg.team2 fgmTeam.own.agg.per100.team1 
                 0.128993429                  0.146998180                 -0.017874344                  0.024184206 
astTeam.opp.agg.per100.team2 fgmTeam.own.agg.per100.team2          fgpct.opp.agg.team1         fg2pct.opp.agg.team1 
                -0.025721938                 -0.037787953                 -0.112972485                  0.125328958 
         fgpct.opp.agg.team2 
                 0.083558381 # this was based on the model with incorrect sf
                 
                 (Intercept)         locationGame.team1.H                net_rtg.team2                net_rtg.team1 
                 0.241556839                 -0.753727302                  0.055064672                 -0.067630326 
                winpct.team1                 winpct.team2 ptsTeam.own.agg.per100.team1 ptsTeam.own.agg.per100.team2 
                -0.388079617                  0.893806034                 -0.007433524                  0.019394157 
stlTeam.own.agg.per100.team1 blkTeam.own.agg.per100.team2          fgpct.own.agg.team2          fgpct.own.agg.team1 
                -0.041243778                  0.041804534                 -0.292957205                 -0.095961197 
        fg2pct.own.agg.team2         fg2pct.own.agg.team1         fg2pct.opp.agg.team2 fgmTeam.own.agg.per100.team1 
                 0.108174904                  0.080581504                 -0.131351823                 -0.014639208 
astTeam.opp.agg.per100.team2 fgmTeam.own.agg.per100.team2          fgpct.opp.agg.team1         fg2pct.opp.agg.team1 
                -0.010596963                 -0.011180280                  0.069454740                  0.009244296 
         fgpct.opp.agg.team2 
                 0.235491669 
 """                
new_coeff =np.array( [   -3.758983993,                -0.543137217 ,                 0.058056140 ,                -0.147293295 ,
                 0.833528317 ,                 0.645713755   ,               0.037281055  ,                0.004321272 ,
                 0.123391322 ,                 0.135187886  ,               -0.222226583  ,               -0.049274726 ,
                 0.140243916  ,                0.095196635 ,                -0.010182367  ,               -0.047588377 ,
                 0.022078144  ,               -0.036728183  ,               -0.167918902  ,                0.083051207 ,
                 0.081332597  ])             

testszn = '2018-19'
betszn = '2020-21'

def arb(odds1,odds2):
    if 1/odds1 + 1/odds2 <1:
        print("An Arb exists with ratio:")
        bet2 = odds1/odds2
        ret1 = odds1
        ret2 = odds2 *bet2
        print("bet the ratio of", "$1 at ", odds1, "to return", ret1, "and bet",
              format(bet2,'.2f'), "at odds", odds2, "to return", format(ret2,'.2f'), "with total outlay", 1+bet2)
    else:
        print("No arbitrage exists")

#scbd = scoreboardv2.ScoreboardV2(day_offset = 1, game_date = ).get_data_frames()[0]
def game_leading_stats(team1,team2,team1_home,szn):# gives stats in the format for winprob, team1_home is 1 for home
    pctstats_team1 = pct(team1,szn)
    pctstats_team2 = pct(team2,szn)
    winpct_team1 = pctstats_team1[0]
    winpct_team2 = pctstats_team2[0]
    fgpct_team1 = pctstats_team1[1]
    fgpct_team2 = pctstats_team2[1]
    per100s_team1 = per100(team1,szn)
    per100s_team2 = per100(team2,szn)
    ptsteam1_per100 = per100s_team1[1]
    ptsteam2_per100 = per100s_team2[1]
    stlteam1_per100 = per100s_team1[2]
    #stlteam2_per100 = per100s_team2[2]
    #blkteam1_per100 = per100s_team1[3]
    blkteam2_per100 = per100s_team2[3]
    fgmteam1_per100 = per100s_team1[4]
    fgmteam2_per100 = per100s_team2[4]
    net_rtg_team2 = enetrtg(team2,szn) ##############3needs updating to net rating
    net_rtg_team1 = enetrtg(team1,szn)
    fg2pct_team1 = fg2pct(team1,szn)
    fg2pct_team2 = fg2pct(team2,szn)
    opp1_shooting = fg2pctopp(team1,szn)
    opp2_shooting = fg2pctopp(team2,szn)
    opp_fg2pct_team1 = opp1_shooting[0]
    opp_fg2pct_team2 = opp2_shooting[0]
    opp_fgpct_team1 = opp1_shooting[1]
    opp_fgpct_team2 = opp2_shooting[1]
    opp_ast_team2_per100 = oppastper100(team2,szn)[0]
    return (1,team1_home,float(net_rtg_team2),float(net_rtg_team1),float(winpct_team1),float(winpct_team2),float(ptsteam1_per100),
            float(ptsteam2_per100 ),  float(stlteam1_per100),float(blkteam2_per100),float(fgpct_team2),float(fgpct_team1),
            float(fg2pct_team2),float(fg2pct_team1),float(opp_fg2pct_team2),float(fgmteam1_per100),float(opp_ast_team2_per100),
            float(fgmteam2_per100),float(opp_fgpct_team1),float(opp_fg2pct_team1),float( opp_fgpct_team2))
    
def winprob(game,coefficients):
    l_score = sum(coefficients*game) #gives logistic score for the game
    odds_model = math.exp(l_score)
    prob_w = 1-( odds_model/(1+odds_model)) 
    return prob_w # for team1 in game stats


def kelly8(home,away,odds_home,odds_away,betfair = 1, szn='2020-21',coefficients = coeff): #takes odds as aussie bet 1.90 for bookmakers 50/50
    arb(odds_home,odds_away)
    #print(Injuries)
        #print("past both injury statements")
    if betfair ==1:
            odds_home = (odds_home-1)*0.95+1
            odds_away = (odds_away-1)*0.95+1
    #print("missed injuries")
    stats = game_leading_stats(home,away,1,szn)
    stats2 = game_leading_stats(away,home,0,szn)
    home_win_prob = (winprob(stats,coefficients)+1-winprob(stats2,coefficients) +winprob(stats,new_coeff))*1/3  #"""+1-winprob(stats2,new_coeff)"""
    #new_win_prob_h = winprob(stats,new_coeff)
    #new_win_prob_a = 1-new_win_prob_h
    away_win_prob = 1- home_win_prob
    c1 = False
    c2 = False 
    if home_win_prob> 1/odds_home:
        c1 = True
        betteam = home
        betodds = odds_home
        kelly = (home_win_prob*odds_home - 1)/(8*(odds_home-1))
        #print("New win prob is ",new_win_prob_h)
        print("Please bet", kelly,"on team", home,"to beat", away, "at effective odds", format(odds_home,'.3f'), 'with winprob', home_win_prob)
    if away_win_prob > 1/odds_away:
        c2 = True
        betteam=away
        betodds = odds_away
        kelly = (away_win_prob*odds_away - 1)/(8*(odds_away-1))
        #print("New win prob is ",new_win_prob_a)
        print("Please bet", kelly,"on team", away,"to beat", home, "at effective odds", format(odds_away,'.3f'), 'with winprob', away_win_prob)
    elif not c1 and not c2:
        betteam ="NIL"
        kelly = 0
        betodds = 0
        print("No bets worth their salt")
    #print("Have you checked season!")
    injuries(teamcity(home))
    injuries(teamcity(away))
    ifwin = kelly*betodds
    b = (home,format(odds_home,'.2f'),away,format(odds_away,'.2f'),format(home_win_prob,'.3f'),betteam,format(kelly,'.4f'),format(betodds,'.2f'),ifwin)
    print(b)
    
    return b
    
def kellytest(odds,prob):
    bet = (prob*odds - 1)/(odds-1) # this is the refined version, based on odds of 1.90 for bookmakers 50/50
    return bet
    #print("no good bets")
def teamid(abb): # returns team ids
    team = [x for x in teams if x['abbreviation'] == abb][0]
    teamID = team['id']
    return teamID

def teamcity(abb):
    team = [x for x in teams if x['abbreviation'] == abb][0]
    teamcity = team['city'].upper()
    return teamcity



def per100(abb,szn): # all per100 stats for a single team, don't forget to update season
    data = teamdashboardbyteamperformance.TeamDashboardByTeamPerformance(team_id = teamid(abb),per_mode_detailed = 'Per100Possessions',season = szn).get_data_frames()[0]
    assper100 = data.AST
    ptsper100 = data.PTS
    stper100=data.STL
    blper100 = data.BLK
    fgmper100 = data.FGM
    return assper100, ptsper100,stper100,blper100,fgmper100

def pct(abb,szn): # percentage based stats, ie winpc and fgpct, dont forget to update aseasn
    data = teamdashboardbyteamperformance.TeamDashboardByTeamPerformance(team_id = teamid(abb),season = szn).get_data_frames()[0]
    winpct = data.W_PCT
    fgpct = data.FG_PCT
    return winpct, fgpct

def fg2pct(abb,szn): # fg2pct, update season
    data = leaguedashteamptshot.LeagueDashTeamPtShot(team_id_nullable = teamid(abb), season = szn).get_data_frames()[0]
    return data.FG2_PCT

def fg2pctopp(abb,szn): # opponent shooting stats, update season
    data = leaguedashoppptshot.LeagueDashOppPtShot(team_id_nullable = teamid(abb),season = szn).get_data_frames()[0]
    return data.FG2_PCT,data.FG_PCT

def enetrtg(abb,szn): # estimated net rating, update season, needs to be changed to real net rating
    data = teamestimatedmetrics.TeamEstimatedMetrics(season = szn).get_data_frames()[0]
    teamrtg = data[data["TEAM_ID"] ==teamid(abb)].E_NET_RATING
    return teamrtg

def oppastper100(abb,szn): # update season, oppo ast per 100 by iteration - this takes the longest
    GP = 0
    weighted_assists = 0
    listboi = [teams[i[0]]["id"] for i in enumerate(teams)]
    x=0
    for item in listboi:
        if item != teamid(abb):
            x=x+1
            if x<31:
                data_per_team = teamdashboardbyopponent.TeamDashboardByOpponent(team_id = item, opponent_team_id = teamid(abb), season = szn, per_mode_detailed = 'Per100Possessions').get_data_frames()[0]
                if len(data_per_team) >0:
                    weighted_assists = data_per_team.GP * data_per_team.AST + weighted_assists
                    GP = GP + data_per_team.GP
                #print(float(weighted_assists), int(GP))
                nba_cooldown = random.gammavariate(alpha=9, beta=0.4)
                time.sleep(nba_cooldown)
            else:
                print("counter stopped")
        else:
            print("Didnt play myself")
    opp_assper100 = weighted_assists/GP
    return opp_assper100,weighted_assists, GP






def assper100(abb): # superfluous
    datafr = teamdashboardbyteamperformance.TeamDashboardByTeamPerformance(team_id = teamid(abb),season = '2018-19',per_mode_detailed = 'Per100Possessions').get_data_frames()[0]
    assper100 = datafr.AST
    return assper100

def winpct(abb):# winpct, superfluous
    data = teamdashboardbyteamperformance.TeamDashboardByTeamPerformance(team_id = teamid(abb),season = '2018-19').get_data_frames()[0]
    winpct = data.W_PCT
    return winpct

ATL = "ATL"
BOS = "BOS"
CLE = "CLE"
NOP = "NOP"
CHI = "CHI"
DAL = "DAL"
DEN = "DEN"
GSW = "GSW"
HOU = "HOU"
LAC = "LAC"
LAL= "LAL"
MIA="MIA"
MIL="MIL"
MIN= "MIN"
BKN= "BKN"
NYK=  "NYK"
ORL= "ORL"
IND= "IND"
PHI= "PHI"
PHX= "PHX"
POR= "POR"
SAC= "SAC"
SAS= "SAS"
OKC= "OKC"
TOR = "TOR"
UTA= "UTA"
MEM= "MEM"
WAS= "WAS"
DET= "DET"
CHA= "CHA"

b = betszn

        
        
        
    
