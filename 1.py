# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 20:46:39 2019

@author: yashw
"""
#import modules
import pandas as pd
import numpy as np
import glob 
import yaml
import matplotlib.pyplot as plt 
import seaborn as sns 
%matplotlib inline
sns.set_style("darkgrid")
plt.rcParams['figure.figsize'] = (14, 8)


#Importing the data
path =r'C:/Users/yashw/Downloads/IPL' # use your path
allFiles = glob.glob(path + "/*.yaml")
allfiles_=[]

for files in allFiles:
    dftemp=files.partition("\\")
    allfiles_.append(dftemp[0]+"/"+dftemp[2])

frame = pd.DataFrame()
list_ = []
for files in allfiles_:
    with open(files, 'r') as f:
        df = pd.io.json.json_normalize(yaml.load(f))
    print(df)
    list_.append(df)
frame = pd.concat(list_)

#cleaning the imported Data
frame.drop('innings',inplace=True, axis=1)
frame.drop('meta.data_version',inplace=True, axis=1)
frame.drop('meta.revision',inplace=True, axis=1)
frame.drop('info.competition',inplace=True, axis=1)
frame.drop('info.gender',inplace=True, axis=1)
frame.drop('info.match_type',inplace=True, axis=1)
frame.drop('info.overs',inplace=True, axis=1)
frame.drop('meta.created',inplace=True, axis=1)
frame=frame.rename(columns={'info.city':'City','info.date':'Year','info.neutral_venue':'Neutral_Venue','info.outcome.by.runs':'By_Runs','info.outcome.by.wickets':'By_Wickets','info.outcome.eliminator':'Eliminator','info.outcome.method':'Method','info.outcome.result':'Result','info.outcome.winner':'Winner','info.player_of_match':'Player_Of_Match','info.teams':'Teams','info.toss.decision':'Toss_Decision','info.toss.winner':'Toss_Winner','info.umpires':'Umpires','info.venue':'Venue'})


list_=frame["Teams"]
res1, res2 = map(list, zip(*list_)) 

frame["Team1"]=res1
frame["Team2"]=res2
frame.drop('Teams',inplace=True,axis=1)

list_=frame["Umpires"]
res1, res2 = map(list, zip(*list_)) 

frame["Umpire1"]=res1
frame["Umpire2"]=res2
frame.drop('Umpires',inplace=True,axis=1)

frame['info.dates'] = frame['info.dates'].apply(lambda x: pd.to_datetime(x[0]))
frame['Year']=pd.DatetimeIndex(frame['info.dates']).year

#Deleting extra Variables 
del res1
del res2
del path

#Computations 

frame.describe()
frame.info()
    
Season=frame['Year'].unique()
print(np.sort(Season))

MaxRunWin=frame.loc[frame['By_Runs']==frame['By_Runs'].max()]
print(MaxRunWin)

MaxWicketWin=frame.loc[frame['By_Wickets']==frame['By_Wickets'].max()]
print(MaxWicketWin)

TossMatchWinner = frame['Toss_Winner'] == frame['Winner']
TossMatchWinner.groupby(TossMatchWinner).size()


#Visualization
sns.countplot(x='Year', data=frame)
plt.title('Matched Playes Per Season')
plt.show()

data = frame.Winner.value_counts()
sns.barplot(y = data.index, x = data, orient='h',);
plt.title('Team Wise Performance')
plt.show()

sns.countplot(TossMatchWinner);
plt.title('Toss Winner is Match Winner')
plt.show()

fig, ax = plt.subplots()
ax.set_title("Winning by Runs - Team Performance")
sns.boxplot(y = 'Winner', x = 'By_Runs', data=frame[frame['By_Runs']>0], orient = 'h'); 
plt.show()

fig, ax = plt.subplots()
ax.set_title("Winning by Wickets - Team Performance")
sns.boxplot(y = 'Winner', x = 'By_Wickets', data=frame[frame['By_Wickets']>0], orient = 'h'); 
plt.show()


