#Import the relevant modules.
#To install understat module use the following link: https://github.com/amosbastian/understat (Thanks Amos Bastian).
#The 5 modules are required to pull the information from Understat and build dataframes.
import asyncio
import aiohttp
from understat import Understat
import pandas as pd

async def main():
    #Plug in with Understat.
    
    async with aiohttp.ClientSession() as session:
        understat = Understat(session)
        
        #Pull the team data into a dataframe by using the team name and year.
        results = await understat.get_team_results("Arsenal",2019)
        df = pd.DataFrame(results)
        
        #Export the data into xlsx format
        df.to_excel("ARS2019-20.xlsx")

#Close the function.
loop = asyncio.get_event_loop()
loop.run_until_complete(main())


#Need to clean the data in the exported table to conduct the analysis.
#Main work here involves splitting out the goals and xG numbers as well as assigning them to the correct team. Use the text to columns feature in excel to do this.
#The xlsx files on the github page show your the final output.
#Require the current and previous session to build full 10-game rolling averages.