#Modules required to build dataframe and plot charts.
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import xticks

#Pull data from the cleansed xlsx.
team_data = pd.read_excel(r"C:\Users\jpc31\eclipse-workspace\seasonrestart\ARS_19_20_Seasons.xlsx")

#Convert table into datafram.
df = pd.DataFrame(team_data)

#Building the rolling averages involves taking the average of 10 matches of goals/xG.
df["Goal_Scored_Rolling_Average_10_Games"] = (df.iloc[:,8].rolling(window=10).mean())
df["Goals_Conceded_Rolling_Average_10_Games"] = (df.iloc[:,9].rolling(window=10).mean())
df["xG_For_Rolling_Average_10_Games"] = (df.iloc[:,10].rolling(window=10).mean())
df["xG_Against_p90_Rolling_Average_10_Games"] = (df.iloc[:,11].rolling(window=10).mean())

#Create the graph - this one is for rolling goals.
#Select the limits for the graph y-axis is for xG/Goal.
#x-axis is the matches, this is taken from the index column of the dataframe.
plt.figure(figsize=[15,10])
plt.ylim(0,3.5)
plt.xlim(38,65)
plt.grid(True)

#Plot the graphs with the rolling average for goals for and against. xG examples hashed out.
plt.plot(df["Goal_Scored_Rolling_Average_10_Games"],label='Goals For')
plt.plot(df["Goals_Conceded_Rolling_Average_10_Games"], label='Goals Against')
#plt.plot(df["xG_For_Rolling_Average_10_Games"],"--",label='xG For')
#plt.plot(df["xG_Against_p90_Rolling_Average_10_Games"],"--",label='xG Against')

#Plot the legend and label the graphs.
plt.legend(loc=1)
ax = plt.gca()
ax.set(ylabel="Goals",xlabel="2019/20 Season",title="Arsenal 10-Game Rolling Avg.")

#Mark the x-axis with managerial changes or blank it out.
#Show the graph.   
xticks([38,53,58],["Emery","Ljungberg","Arteta"],rotation = "30", ha="center")
plt.show()
