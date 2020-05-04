#Import the relevant modules.
#Initial 5 modules are required to pull the information from Understat and build dataframes.
#Final 2 are used to plot the graphs using matplotlib.

import asyncio
import aiohttp
from understat import Understat
import pandas as pd
from pandas import json_normalize
import matplotlib.pyplot as plt
from matplotlib.pyplot import xticks

#Manipulation of the the data and the graphs plots are done within the function that pulls the data from Understat.
#Let me know if there's a better way to do this.

async def main():
    #Plug in with Understat.
    
    async with aiohttp.ClientSession() as session:
        understat = Understat(session)
        
    #Pull the player data into a table. '647' is the player ID as applied by Understat.
    #647 is the ID for Harry Kane. Aguero's ID: 619, Salah's ID: 1250. Find others IDs and plot their data.
      
        player = await understat.get_player_matches(647)
        player_stats = json_normalize(player)
        
    #Run print(player_stats) to see the information that is obtained.
    #Data is pulled as strings and needs to be converted to type float.
    #Try playing with other data besides goals such as assists and combined goal and assist totals.
         
        player_stats["goals_flt"] = player_stats["goals"].astype(float)
        player_stats["time_flt"] = player_stats["time"].astype(float)
        player_stats["xG_flt"] = player_stats["xG"].astype(float)
        player_stats["shots_flt"] = player_stats["shots"].astype(float)
        
    #Need to convert season from the year it starts (2019) to the common format (2019/10).
                        
        player_stats["season_int"] = player_stats["season"].astype(int)
        player_stats["season_id"] = (player_stats["season_int"]).astype(str) + "/" + (player_stats["season_int"] + 1).astype(str)

    #Build a table with the data required.
    #Convert that table into a dataframe for analysis.
    #Print the dataframe to see the information. 
        
        player_stats = player_stats[["date","season_int","season_id","time_flt","goals_flt","xG_flt","shots_flt"]]
        df = pd.DataFrame(player_stats)
        
    #For 2015/16 onwards, remove some 2014/15 data but still require 15 data points before the seasons for the rolling average.
    #Change order the dataframe by date.
        
        df = df[:-20]
        df = df.sort_values(by=["date"],ascending=True)
        
    #Building the rolling averages involves taking the sum of 15 matches of goals/xG/shots.
    #Then Diving that by the total minutes divided by 90 to get the p90 rolling average metric.
        
        df["Goals_p90_Rolling_Average_15_Games"] = (df.iloc[:,4].rolling(window=15).sum()) / (df.iloc[:,3].rolling(window=15).sum() / 90)
        df["xG_p90_Rolling_Average_15_Games"] = (df.iloc[:,5].rolling(window=15).sum()) / (df.iloc[:,3].rolling(window=15).sum() / 90)
        df["Shots_p90_Rolling_Average_15_Games"] = (df.iloc[:,6].rolling(window=15).sum()) / (df.iloc[:,3].rolling(window=15).sum() / 90)
        df["xG_per_Shot_Rolling_Average_15_Games"] =  df["xG_p90_Rolling_Average_15_Games"] / df["Shots_p90_Rolling_Average_15_Games"]
               
    #Create the graph - this one is for goals and xG per 90. Use the same for shots and xG per Shot.
    #Select the limits for the graph y-axis is for xG/Goal.
    #x-axis is the matches, this is taken from the index column of the dataframe.    
        
        plt.figure(figsize=[15,10])
        plt.ylim(0, 1.5)
        plt.xlim(0,152)
        plt.grid(True)
        
    #Plot the graphs with the rolling average. 
    #Plot the legend and label the graphs.    
        
        plt.plot(df["Goals_p90_Rolling_Average_15_Games"],label='Goals p90 Rolling Avg.')
        plt.plot(df["xG_p90_Rolling_Average_15_Games"],label='xG p90 Rolling Avg.')
        plt.legend(loc=2)
        ax = plt.gca()
        ax.set(ylabel="xG/Goals p90",xlabel="Season",title="Harry Kane")
        
    #Mark the x-axis with the seasons. Identify in the dataframe the index number where the season changes. Can do this with injuries.
    #Invert the x-axis to show the oldest to the latest season.
    #Show the graph.   
        
        xticks([152,114,84,47,19],["2015/16", "2016/17", "2017/18","2018/19","2019/20"], ha="center")
        '''xticks([110,93,76,56,26,22,0],["Ankle Sep '16", "Ankle Mar '16", "Hamstring Oct '17", "Ankle Mar '18","Ankle Jan '19", 
        "Ankle Apr '19","Thigh Jan '20"], rotation = "30", ha="right")'''
        ax.invert_xaxis()
        plt.show()
        
#Close the function.        
        
loop = asyncio.get_event_loop()
loop.run_until_complete(main())