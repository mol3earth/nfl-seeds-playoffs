#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  2 18:41:26 2020
@author: mol3earth
"""

from requests import get
from bs4 import BeautifulSoup as bs4

debugMode=True
baseUrl = 'https://en.m.wikipedia.org/'

class playOffSeedsAndStrengthOfSchedule:
    '''
        play off seeds and strength of schedule
        stores the structure created and the print summary functions
    '''
    
    def __init__(self):
        self.playOffStr = {}    
    
    def printSoSbySeed(self):
        '''
        Will print the mean Strength of Schedule for each Seed
        '''
        print('-'*50)
        print('Strength of Schedule by Seed')
        print('-'*50)
        pp='\t'
        print('Seed  ' + 'MaxSoS '+' MinSoS '+' AvgSoS')
        SoSbS=[]
        for n in range(0,7):
            SoSbS.append([]);  
        for k in self.playOffStr.keys():
            for seed in range(1,7):
                SoSbS[seed].append(int(self.playOffStr[k]['Seeding']['AFC'][seed]['SoS']['Rank']))
                SoSbS[seed].append(int(self.playOffStr[k]['Seeding']['NFC'][seed]['SoS']['Rank']))
        for seed in range(1,7):
            print(str(seed)+'  '+pp+'\t'.join([
                                 str(min(SoSbS[seed])),
                                 str(max(SoSbS[seed])),
                                 str(sum(SoSbS[seed])/len(SoSbS[seed]))[0:4]
                  ]))
        
    def printSoSByYear(self):
        '''
        Will print the Strength of Schedules of each team by year.
        '''
        print('-'*50)
        print('Strength of Schedule by Year')
        print('-'*50)
        pp='\t'
        tArr={}
        tArr['max']=[]
        tArr['min']=[]
        tArr['avg']=[]
        print(' Year         ' + 'MaxSoS '+' MinSoS '+' AvgSoS')
        for k in self.playOffStr.keys():
            tArr[k]=[]
            for team in self.playOffStr[k]['POSoS'].keys():
                tArr[k].append( int(self.playOffStr[k]['POSoS'][team]) )
            tArr['max'].append(max(tArr[k]))
            tArr['min'].append(min(tArr[k]))
            tArr['avg'].append(sum(tArr[k])/len(tArr[k]))
            print(k+'  '+pp+'\t'.join( [str(min(tArr[k])),
                                 str(max(tArr[k])),
                                 str(sum(tArr[k])/len(tArr[k]))[0:4]
                 ]))
        print('Averages'+pp+'\t'.join( [str(sum(tArr['min'])/len(tArr['min']))[0:4],
                             str(sum(tArr['max'])/len(tArr['max']))[0:4],
                             str(sum(tArr['avg'])/len(tArr['avg']))[0:4]
              ]))
    
    def printSoSWinLossAndDiffByRoundAndSeed(self):
        '''
        Will print the Wins, Losses, and SoS Differential for each round in the playoffs. 
        '''
        print('-'*50)
        print('Average Strength of Schedule of Winners (AWSoS)\n' +
              'Average Strength of Schedule of Losers (ALSoS)\n' +
              'Average Strength of Schedule of Winners (ADSoS)\n' +
              'by Round and by Seed')
        print('-'*50)
        wbSoS={};    lbSoS={};    dbSoS={}    
        wbrSoS={};    lbrSoS={};    dbrSoS={} 
        for rnd in ['WC','DV','CC','SB']:
            wbrSoS[rnd]=[] ; lbrSoS[rnd]=[] ; dbrSoS[rnd]=[] ; 
        wbsSoS=[];    lbsSoS=[];    dbsSoS=[];
        pp='\t'
        for n in range(0,7):
            wbsSoS.append([]);    lbsSoS.append([]);    dbsSoS.append([]);
        for k in self.playOffStr.keys():
            wbSoS[k]=[]
            lbSoS[k]=[]
            dbSoS[k]=[]
            for rnd in self.playOffStr[k]['roundStr']:
                for game in self.playOffStr[k]['roundStr'][rnd]:
                    wSoS = int(game['Winner']['SoS'])
                    lSoS = int(game['Loser']['SoS'])
                    dSoS = lSoS - wSoS
                    wbSoS[k].append(wSoS)
                    lbSoS[k].append(lSoS)
                    dbSoS[k].append(dSoS)
                    wbrSoS[rnd].append(wSoS)
                    lbrSoS[rnd].append(lSoS)
                    dbrSoS[rnd].append(dSoS)
                    wbsSoS[game['Winner']['Seed']].append(wSoS)
                    lbsSoS[game['Winner']['Seed']].append(lSoS)
                    dbsSoS[game['Winner']['Seed']].append(dSoS) 
                    
            #print(k+'  '+pp+'\t'.join( [
            #             str(sum(wbSoS[k])/len(wbSoS[k]))[0:4],
            #             str(sum(lbSoS[k])/len(lbSoS[k]))[0:4],
            #             str(sum(dbSoS[k])/len(dbSoS[k]))[0:4],
            #             ]))
        headers = pp +'\t'.join(['AWSoS','ALSoS','ADSoS'])
        print('Rnd' + headers)
        for rnd in wbrSoS.keys():
            print(rnd+'  '+pp+'\t'.join( [
                 str(sum(wbrSoS[rnd])/len(wbrSoS[rnd]))[0:4],
                 str(sum(lbrSoS[rnd])/len(lbrSoS[rnd]))[0:4],
                 str(sum(dbrSoS[rnd])/len(dbrSoS[rnd]))[0:4],
                 ]))
        print('')
        print('Seed' + headers)
        for seed in range(1,7):
            print(str(seed)+'  '+pp+'\t'.join( [
                 str(sum(wbsSoS[seed])/len(wbsSoS[seed]))[0:4],
                 str(sum(lbsSoS[seed])/len(lbsSoS[seed]))[0:4],
                 str(sum(dbsSoS[seed])/len(dbsSoS[seed]))[0:4],
                 ]))
        
    def printAll(self):
        self.printSoSbySeed()
        self.printSoSByYear()
        self.printSoSWinLossAndDiffByRoundAndSeed()

def getSoS(table):
    '''
    Parses Strength of Schedule information for each team.
    '''
    SoS = {}
    for row in table.find_all('tr')[1:]:
        cols = row.find_all('td')
        team = cols[1].text.split('(')
        record = team[1].strip(')')
        team = team[0].strip()
        SoS[team] = {
                'Rank': cols[0].text,
                'Final Record': record,
                'Rate': cols[2].text,
                'High': cols[3].text,
                'Low' : cols[4].text,
                'Last': cols[5].text
                }
    return SoS

def findSoS(SoS,seedStr):
    '''
    Combines wikipedia information with SoS information.
    '''
    SoSlist = {}
    for SoSteam in SoS.keys():
        SoStm = SoSteam.split()
        SSidx = -1
        for conf in ['NFC','AFC']:
            for seedID in range(1,7):    
                seedTm = seedStr[conf][seedID]['team'].split()
                SDidx = -1
                for n in range(0,len(seedTm)):
                    #print('  '+ seedTm[SDidx] + ' --- ' + SoStm[SSidx])
                    if seedTm[SDidx] == SoStm[SSidx]:
                        if debugMode:
                            print('!!foundMatch!!')
                            print('  '+ seedTm[SDidx] + ' --- ' + SoStm[SSidx])
                        seedStr[conf][seedID]['SoS'] = SoS[SoSteam]
                        SoSlist[seedStr[conf][seedID]['team']] =  SoS[SoSteam]['Rank']
                        break
                    SDidx-=1
    return seedStr, SoSlist

def getTeamInfo(wikiUrl):
    '''
    Gets teams record from team-year wikipedia page.
    '''
    debugMode=False
    if debugMode:
        print('\n   '+ ' scraping: ' + wikiUrl)
    infoTableRows = bs4( 
                        get( baseUrl + wikiUrl ).text,
                        features="html5lib" 
                        ).find(
                                'table' , 
                                {'class': 'infobox vcard'} 
                               ).find_all('tr')
    noID = True
    resultID = 0
    while noID:
        resultID += 1
        noID = not ('Results' in infoTableRows[ resultID ].text) 
        if debugMode:
            try:
                print('\n ' + '-'*25 +' \n\n' + infoTableRows[ resultID ].prettify() +'\n  ----- ')
            except:
                print('\n ' + ' - WHOLE DUMP -'*25 +' \n\n' + str(infoTableRows).replace(',','\n') + '\n  ----- ' )
    if debugMode:
        print('    ' + 'found resultID = ' + str(resultID) + '  at  ' +baseUrl + wikiUrl)
    rID = resultID+1
    dID = resultID+2
    try: 
        dPlace = infoTableRows[dID].find('a').text
    except:
        dPlace = infoTableRows[dID].find('td').text
    record = infoTableRows[rID].find('td').text
    return dPlace, record
    
def getSeeding(table):
    seedStr = {}
    seedStr['AFC'] = []
    seedStr['NFC'] = []
    seedStr['Seeds'] = []
    seedStr['Seeds'].append('')
    seedStr['AFC'].append('')
    seedStr['NFC'].append('')
    rows= table.find_all('tr')
    if rows[1].find_all('th')[1].text == 'AFC':
        AFC = 1
        NFC = 2
    elif rows[1].find_all('th')[1].text == 'NFC':
        AFC = 2
        NFC = 1
    for n in range(1,7):
        tds = rows[n+1].find_all('td')
        AFCtm = tds[AFC].find_all('a')
        NFCtm = tds[NFC].find_all('a')
        At = AFCtm[0].text
        Aw = AFCtm[0]['href']
        Nt = NFCtm[0].text
        Nw = NFCtm[0]['href']   
        Nd , Nr = getTeamInfo(Nw)    
        Ad , Ar = getTeamInfo(Aw)       
        seedStr['Seeds'].append({ 'AFC':At, 'NFC':Nt })
        seedStr['AFC'].append({ 'team':At, 'div':Ad, 'rec':Ar, 'wiki':Aw })
        seedStr['NFC'].append({ 'team':Nt, 'div':Nd, 'rec':Nr, 'wiki':Nw })
    print(str(seedStr).replace("[",'').replace("]",'').replace(":",'').replace("'",'').replace(',','').replace('{','\n').replace('}','\n').replace("team",'  ').replace("rec",'-').replace("wiki",'').replace("div",'\t  ') )
    return seedStr  

def getSeed(team, seeds):
    if debugMode:
        print('  finding team: ' + team + ' in seedsStr' )
    for seed in seeds[1:]:
        if team in seed.values():
            outSeed = seeds.index(seed)
    return outSeed

def getRoundsByScheduleTable(table, seeds, SoS):
    '''
    Scrapes the relevant information from wikipidea post 2007 structure.
    '''
    if debugMode:
        print(table.prettify())
    games = table.find_all('tr')
    winsBySoS, winsBySeed, roundsBySeed, roundStr = initStuff()
        #      WC Rnd     Div Rnd      CC Rnd    SB
    for n in [ 2,3,4,5,   7,8,9,10,     12,13,   15 ] :
        Cols = games[n].find_all('td')
        AwayTeam = Cols[0]
        Score = Cols[1].text
        HomeTeam = Cols[2]
        DateTime = Cols[3].text + ' ' + Cols[4].text
        if debugMode:
            print('\n   AT: ' + AwayTeam.text + '\n   HT: ' + HomeTeam.text )
        if AwayTeam.find('b') == None:
            Winner = { 'Team': HomeTeam.text,
                       'Seed': getSeed(HomeTeam.text, seeds),
                       'SoS':  SoS[HomeTeam.text],
                       'Home': True                                                   
                      }
            Loser = {  'Team': AwayTeam.text,
                       'Seed': getSeed(AwayTeam.text, seeds),
                       'SoS':  SoS[AwayTeam.text],
                       'Home': False                                                   
                      }
        else: 
            Winner = { 'Team': AwayTeam.text,
                       'Seed': getSeed(AwayTeam.text, seeds),
                       'SoS':  SoS[AwayTeam.text],
                       'Home': False                                                   
                      }
            Loser = {  'Team': HomeTeam.text,
                       'Seed': getSeed(HomeTeam.text, seeds),
                       'SoS':  SoS[HomeTeam.text],
                       'Home': True                                                   
                      }
        if n < 6:
            rnd = 'WC'
        elif n < 11:
            rnd = 'DV'
        elif n < 15:
            rnd = 'CC'
        else :
            rnd = 'SB'
        winsBySoS, winsBySeed, roundsBySeed, roundStr = popStuff(Winner, Loser, winsBySeed, winsBySoS, rnd, roundsBySeed, roundStr, Score, DateTime)
    return winsBySoS, winsBySeed, roundsBySeed, roundStr

def initStuff():    
    winsBySeed=[0]*7
    winsBySoS=[0]*32
    roundsBySeed={}
    roundsBySeed['WC']=[0]*7
    roundsBySeed['DV']=[0]*7
    roundsBySeed['CC']=[0]*7
    roundsBySeed['SB']=[0]*7
    roundStr = {}
    roundStr['WC'] = []
    roundStr['DV'] = []
    roundStr['CC'] = []
    roundStr['SB'] = []
    return winsBySoS, winsBySeed, roundsBySeed, roundStr

def popStuff(Winner, Loser, winsBySeed, winsBySoS, rnd, roundsBySeed, roundStr, Score, DateTime):
    winsBySeed[Winner['Seed']] +=1
    winsBySoS[int(Winner['SoS'])] +=1
    roundsBySeed[rnd][Winner['Seed']] +=1
    roundStr[rnd].append({ 'Winner': Winner , 
                            'Loser': Loser , 
                            'Date' : DateTime ,
                            'Score' : Score
                        })
    return winsBySoS, winsBySeed, roundsBySeed, roundStr

def Hparse(h4, DateTime, seeds, SoS):
    '''
    strips years and round information from the matchup titles.
    '''
    tempTeams=h4.text
    for string in ['Super','Bowl','XXX', 'XLI', 'XL', 'XI', 'IX', 'VIII', 'VII', 'Edit', '(3OT)', '(2OT)', '(OT)', 'NFC' , 'AFC', 'Championship', ':' ]:
        tempTeams = tempTeams.replace( string , '' )
    #teams = h4.text.replace('Super','').replace('Bowl',''),replace('XXXVIII','').replace('Edit','').replace('(3OT)','').replace('(2OT)','').replace('(OT)','').replace('NFC','').replace('AFC','').replace('Championship','').replace(':','').strip().split(', ')
    teams = tempTeams.strip().split(', ')
    WinTm = ' '.join(teams[0].split(' ')[:-1])
    WinScore = teams[0].split(' ')[-1]
    LosTm = ' '.join(teams[1].split(' ')[:-1])
    LosScore = teams[1].split(' ')[-1]
    Score = WinScore + '-' + LosScore
    if debugMode:
        print('  h4 - ' + h4.text)
        print('    raw teams - '+ ', '.join(teams))
        print('    WinTm - '+WinTm)
        print('    LosTm - '+LosTm)
        print('    DT - ' + DateTime)
    Winner, Loser = popWinLos(WinTm, LosTm, seeds, SoS)    
    return Winner, Loser, Score, DateTime

def popWinLos(WinTm, LosTm, seeds, SoS):
    Winner = { 'Team': WinTm,
               'Seed': getSeed( WinTm , seeds),
               'SoS':  SoS[ WinTm ],
               'Home': False                                                   
              }
    Loser = {  'Team': LosTm,
               'Seed': getSeed( LosTm , seeds),
               'SoS':  SoS[ LosTm ],
               'Home': False                                                   
              }
    return Winner, Loser

def getRoundsByManyDivs(divs, seeds, SoS):
    '''
    Scrapes wikipedia pages pre-2007 for the relevant information
    '''
    winsBySoS, winsBySeed, roundsBySeed, roundStr = initStuff()
    for divID in [3, 4, 5, 6]:
        if debugMode:
            print(divID)
            print(divs[divID].find_all('h4'))
        for h4 in divs[divID].find_all('h4'):
            Winner, Loser , Score, DateTime = Hparse(h4 ,  h4.findPrevious('h3').text.strip('Edit'), seeds, SoS)
            if divID == 3:
                rnd = 'WC'
            elif divID == 4 :
                rnd = 'DV'
            elif divID == 5:
                rnd = 'CC'
            winsBySoS, winsBySeed , roundsBySeed, roundStr = popStuff(Winner, Loser, winsBySeed, winsBySoS, rnd, roundsBySeed, roundStr, Score, DateTime)
        if divID == 6:
            Winner, Loser, Score, DateTime = Hparse(divs[6].previousSibling ,  divs[6].find('li').text.replace('Date:','').strip() , seeds, SoS)            
            rnd = 'SB'
            winsBySoS, winsBySeed , roundsBySeed, roundStr = popStuff(Winner, Loser, winsBySeed, winsBySoS, rnd, roundsBySeed, roundStr, Score, DateTime)
        if debugMode:
            print('-*'*50 + '\n       DONE WITH  ' + rnd)
    return winsBySoS, winsBySeed, roundsBySeed, roundStr

def main(yearStart=2003,yearEnd=2018):
    '''
    Takes a range of years and returns a structure of Playoff performance by 
        seed and strenght of schedule. 
        input: 
                yearStart: integer, default is 2003 (playoff restructured to 
                                                     current)
                yearEnd: integer, range end inclusive, defaults to 2018.
    '''
    playOffStr={}
    posasos = playOffSeedsAndStrengthOfSchedule()
    for year in range(yearStart,yearEnd+1):
        if year < 2003:
            print('*'*50 + '\n  CAN NOT GET Strength of Schedule FOR YEARS < 2003 ')
            print('      UNLESS YOU FIND A BETTER SITE THAN teamrankings.com ')
            quit
        if debugMode:
            print('DOING '+str(year))
        yrRng = str(year)+'-'+str(year+1)[-2:]
        playOffStr[yrRng] = {}
        # get SoS 
        sosGet = get('https://www.teamrankings.com/nfl/ranking/schedule-strength-by-other?date=' +
                     str(year+1) + 
                     '-02-28').text
        SoStable = bs4( sosGet , features="html5lib" ).find('table')
        playOffStr[yrRng]['SoS'] = getSoS(SoStable)
        # get Wiki tables
        wikiGet = get(    baseUrl + 
                          "/wiki/" + # + "Template:"
                          str(year) + 
                          "%E2%80%93" + 
                          str(year+1)[-2:] + 
                          "_NFL_playoffs"
                     ).text
        pg = bs4(  wikiGet , features="html5lib" )
        tables = pg.find_all('table', {'class':'wikitable'})                                    # 2
        playOffStr[yrRng]['Seeding'] = getSeeding(tables[0])
        playOffStr[yrRng]['Seeding'], playOffStr[yrRng]['POSoS'] = findSoS(playOffStr[yrRng]['SoS'], playOffStr[yrRng]['Seeding'])
        if year > 2005:                                                                                                                                  ## 4  
            playOffStr[yrRng]['WBSoS'], playOffStr[yrRng]['WBS'], playOffStr[yrRng]['RBS'], playOffStr[yrRng]['roundStr'] = getRoundsByScheduleTable(tables[1], playOffStr[yrRng]['Seeding']['Seeds'] ,  playOffStr[yrRng]['POSoS'])
        else:
            divs = pg.find_all('section', {'class': 'collapsible-block'})
            playOffStr[yrRng]['WBSoS'], playOffStr[yrRng]['WBS'], playOffStr[yrRng]['RBS'], playOffStr[yrRng]['roundStr'] = getRoundsByManyDivs( divs, playOffStr[yrRng]['Seeding']['Seeds'],  playOffStr[yrRng]['POSoS'])
    posasos.playOffStr = playOffStr
    return posasos
