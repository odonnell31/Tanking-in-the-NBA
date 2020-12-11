# -*- coding: utf-8 -*-
"""
Created on Sun Nov 29 15:41:27 2020

@author: ODsLaptop

@title: creating regression dataset
"""

# import libraries
import pandas as pd

# loading nba team data
nba_data = pd.read_csv("https://raw.githubusercontent.com/odonnell31/NBA-Team-Strategies/main/data/nba_team_data_1990_v2.csv")

# create dataframe for only nba finals teams
nba_finals_teams = nba_data[nba_data['Finals_Team'] == 'Y']
nba_finals_teams = nba_finals_teams[nba_finals_teams['Year'] > 1998]
nba_finals_teams = nba_finals_teams.reset_index(drop=True)

# calc years since last losing season, and how many consecutibe losing season
years_since_losing = []
consecutive_years_losing = []

# iterate through all rows in dataframe
for i in range(len(nba_finals_teams)):
    finals_year = nba_finals_teams['Year'][i]
    year_prior = finals_year - 1
    team = nba_finals_teams['Team'][i]
    last_losing_season = 0
    consec_losing_seasons = 0
    # flags
    losing = 0
    
    # if the last season was a losing season:
    if nba_data.loc[(nba_data['Team'] == team) & (nba_data['Year'] == year_prior)]['Losing_season'].values[0] == "Y":
        last_losing_season = year_prior
        consec_losing_seasons += 1
        losing = 1
        year_prior -= 1
        
        # how many consecutive losing seasons were there?
        while losing == 1:
            if nba_data.loc[((nba_data['Team'] == team) & (nba_data['Year'] == year_prior))]['Losing_season'].values[0] == 'Y':
                consec_losing_seasons += 1
                year_prior -= 1
            else:
                losing = 0
    
    # if the last season was a winning season            
    elif nba_data.loc[((nba_data['Team'] == team) & (nba_data['Year'] == year_prior))]['Losing_season'].values[0] == 'N':
        year_prior -= 1
        losing = 0
        
        # work backwards to find the last losing season
        while losing == 0:
            
            # if it wasn't a losing season, keep looking
            if nba_data.loc[((nba_data['Team'] == team) & (nba_data['Year'] == year_prior))]['Losing_season'].values[0] == 'N':
                year_prior -= 1
                losing = 0
            
            # if it was a losing season, flag it
            else:
                last_losing_season = year_prior
                consec_losing_seasons += 1
                year_prior -= 1
                losing = 1
        
        # now, count the consecutive losing seasons      
        while losing == 1:
            if nba_data.loc[((nba_data['Team'] == team) & (nba_data['Year'] == year_prior))]['Losing_season'].values[0] == 'Y':
                consec_losing_seasons += 1
                year_prior -= 1
                losing = 1
            
            # stop counting when they win again
            else:
                losing = 0
            
                    
    years_since_losing.append(finals_year - last_losing_season)
    consecutive_years_losing.append(consec_losing_seasons)
                
nba_finals_teams['years_since_losing_season'] = years_since_losing
nba_finals_teams['consecutive_years_losing'] = consecutive_years_losing

# calc years of consecutive playoff appearances pre-finals appearance
consecutive_playoff_seasons = []

# iterate through all rows in dataframe
for i in range(len(nba_finals_teams)):
    finals_year = nba_finals_teams['Year'][i]
    year_prior = finals_year - 1
    team = nba_finals_teams['Team'][i]
    consec_playoff_seasons = 0
    # flags
    playoffs = 0
    
    # if the last season was a playoffs season:
    if nba_data.loc[(nba_data['Team'] == team) & (nba_data['Year'] == year_prior)]['Playoffs'].values[0] == "Y":
        consec_playoff_seasons += 1
        year_prior -= 1
        playoffs = 1
        
        # how many consecutive playoffs seasons were there?
        while playoffs == 1:
            try:
                if nba_data.loc[((nba_data['Team'] == team) & (nba_data['Year'] == year_prior))]['Playoffs'].values[0] == 'Y':
                    consec_playoff_seasons += 1
                    year_prior -= 1
                else:
                    playoffs = 0
            except:
                print("ran out of seasons...")
                playoffs = 0
    
    else:
        print("The", team, "did not make the playoffs prior to their",
              finals_year, "finals appearance")
                    
    consecutive_playoff_seasons.append(consec_playoff_seasons)
                
nba_finals_teams['consecutive_playoff_seasons'] = consecutive_playoff_seasons

nba_finals_teams.to_csv("nba_finals_teams_data_1990_v2.csv", index=False)