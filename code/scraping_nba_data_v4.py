# -*- coding: utf-8 -*-
"""
Created on Sun Nov 29 10:46:48 2020

@author: Michael ODonnell

@title: scraping NBA team data
"""

# import needed libraries
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

# this function will scrape team performance by year for each specified year
def scrape_NBA_team_data(years = [2017, 2018]):
    
    # first, create empty dataframe with needed column headers
    final_df = pd.DataFrame(columns = ["Year", "Team", "W", "L",
                                       "W/L%", "GB", "PS/G", "PA/G",
                                       "SRS", "Playoffs",
                                       "Losing_season"])
    
    # loop through each year, scraping team performance that year
    for y in years:
        # NBA season to scrape
        year = y
        
        # URL to scrape
        url = f"https://www.basketball-reference.com/leagues/NBA_{year}_standings.html"
        
        # HTML data collected
        html = urlopen(url)
        
        # create beautiful soup object from HTML
        soup = BeautifulSoup(html, features="lxml")
        
        # use getText()to extract the headers into a list
        titles = [th.getText() for th in soup.findAll('tr', limit=2)[0].findAll('th')]
        
        # first, find only column headers
        headers = titles[1:titles.index("SRS")+1]
        
        # then, update the titles list to exclude first set of column headers
        titles = titles[titles.index("SRS")+1:]
        
        # then, grab all row titles (ex: Boston Celtics, Toronto Raptors, etc)
        try:
            row_titles = titles[0:titles.index("Eastern Conference")]
        except: row_titles = titles
        # remove the non-teams from this list
        for i in headers:
            row_titles.remove(i)
        row_titles.remove("Western Conference")
        divisions = ["Atlantic Division", "Central Division",
                     "Southeast Division", "Northwest Division",
                     "Pacific Division", "Southwest Division",
                     "Midwest Division"]
        for d in divisions:
            try:
                row_titles.remove(d)
            except:
                print("no division:", d)
        
        # next, grab all data from rows (avoid first row)
        rows = soup.findAll('tr')[1:]
        team_stats = [[td.getText() for td in rows[i].findAll('td')]
                    for i in range(len(rows))]
        # remove empty elements
        team_stats = [e for e in team_stats if e != []]
        # only keep needed rows
        team_stats = team_stats[0:len(row_titles)]
        
        # add team name to each row in team_stats
        for i in range(0, len(team_stats)):
            team_stats[i].insert(0, row_titles[i])
            team_stats[i].insert(0, year)
            
        # add team, year columns to headers
        headers.insert(0, "Team")
        headers.insert(0, "Year")
        
        # create a dataframe with all aquired info
        year_standings = pd.DataFrame(team_stats, columns = headers)
        
        # add a column to dataframe to indicate playoff appearance
        year_standings["Playoffs"] = ["Y" if "*" in ele else "N" for ele in year_standings["Team"]]
        # remove * from team names
        year_standings["Team"] = [ele.replace('*', '') for ele in year_standings["Team"]]
        # add a column to dataframe to indicate a losing season (win % < .5)
        year_standings["Losing_season"] = ["Y" if float(ele) < .5 else "N" for ele in year_standings["W/L%"]]
        
        # append new dataframe to final_df
        final_df = final_df.append(year_standings)
        
    # print final_df
    print(final_df.info)
    # export to csv
    final_df.to_csv("nba_team_data_1990_v2.csv", index=False)

# test on 2015 and 2016 because 2015 is old format and 2016 is new format
#scrape_NBA_team_data(years = [2015,2016])
   
scrape_NBA_team_data(years = [1990, 1991, 1992, 1993, 1994,
                              1995, 1996, 1997, 1998, 1999,
                              2000, 2001, 2002, 2003, 2004,
                              2005, 2006, 2007, 2008, 2009,
                              2010, 2011, 2012, 2013, 2014,
                              2015, 2016, 2017, 2018, 2019,
                              2020])

def NBA_Final_teams():

    url = "https://www.basketball-reference.com/playoffs/"
    
    # HTML data collected
    html = urlopen(url)
    
    # create beautiful soup object from HTML
    soup = BeautifulSoup(html, features="lxml")
    
    # use getText()to extract the headers into a list
    finals_titles = [th.getText() for th in soup.findAll('tr', limit=2)[1].findAll('th')]
    
    # get rows from table
    rows = soup.findAll('tr')[2:]
    finals_stats = [[td.getText() for td in rows[i].findAll('td')]
                    for i in range(len(rows))]
    # pop the empty row
    finals_stats.pop(20)
    finals_stats = finals_stats[0:38]
    
    # add the years into finals_stats
    last_year = 2020
    for i in range(0, len(finals_stats)):
        finals_stats[i].insert(0, last_year)
        last_year -=1
    
    # create the dataframe
    nba_finals = pd.DataFrame(finals_stats, columns = finals_titles)
    
    nba_finals.to_csv("nba_finals_teams.csv", index=False)
    
#NBA_Final_teams()
