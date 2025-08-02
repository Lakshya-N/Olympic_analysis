#creating the medal_tally to see the number of medals won by each noc ( removing duplicate wrong data)
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt


def medal_tally(df):
    medal_tally=df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])  #drops the ambiguous data
    medal_tally=medal_tally.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()  #creates a df grouped by the regions with the number of gold,silver and bronze won
    medal_tally["Total"]=medal_tally['Gold']+medal_tally['Bronze']+medal_tally['Silver'] #adds a new column to the df to get total number of medals won by that region until now.



    return medal_tally


#creating options for the drop down
#we use numpy as we handle 1d data arrays here
def country_year_list(df):
    year=df['Year'].unique().tolist()
    year.sort()
    year.insert(0,"Overall")

    country=np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0,"Overall")

    return year,country

#medal tally
def fetch_medal_tally(df,year,country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == "Overall" and country == "Overall":
        temp_df = medal_df
    if year == "Overall" and country != "Overall":
        # olympic wise data
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != "Overall" and country == "Overall":
        temp_df = medal_df[medal_df['Year'] == int(year)]
    if year != "Overall" and country != "Overall":
        temp_df = medal_df[(medal_df['Year'] == int(year)) & (medal_df['region'] == country)]
    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                      ascending=True).reset_index()
    x['Total'] = x['Gold'] + x['Silver'] + x['Bronze']
    return x


#overall analysis

#graph of nations participating and year
#selecting every unique year and column
def data_over_time(df,column):
    nations_over_time = df.drop_duplicates(['Year', column])['Year'].value_counts().reset_index().sort_values("Year")
    nations_over_time.rename(columns={'Year':'Edition', 'count': column}, inplace=True)
    return nations_over_time

#people with highest number of medals in each sport

#remove the values where the medal is NaN because it doesnt matter

def most_successfull(df,sport):
     temp_df=df.dropna(subset=["Medal"])
     if sport!="Overall":
         temp_df=temp_df[temp_df['Sport']==sport]
     x=temp_df['Name'].value_counts().reset_index().head(15).merge(df,left_on="Name",right_on="Name",how="left")[['Name','count','Sport','region']].drop_duplicates(subset=['Name'])
     x.rename(columns={'count':"medals"},inplace=True)
     return x

#to pull up the different years and sports

def year_and_sports(df):
    year=df['Year'].unique().tolist()
    year.sort()
    year.insert(0,"Overall")
    sports=df['Sport'].unique().tolist()
    sports.insert(0,"Overall")
    return year,sports


# country wise medal tally

def year_wise_medal_tally(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    temp_df = temp_df[temp_df['region'] == country]
    new_df = temp_df.groupby('Year').count()['Medal'].reset_index()
    return new_df

def country_event_heatmap(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    pt=new_df.pivot_table(index="Sport",columns="Year",values="Medal",aggfunc="count").fillna(0)
    return pt


#top ten atheletes
# top atheletes based on country and based on the sports

def top_athletes(df, country, sport):

    if  sport == "Overall":
        temp_df = df[df['region'] == country]
        top = temp_df['Name'].value_counts().reset_index().head(5).merge(df, left_on="Name", right_on="Name", how="left")[
            ["Name", "Sport","count"]].drop_duplicates()
        top.rename(columns={ 'count':'Medal count'}, inplace=True)
        return top


    if sport != "Overall":
        temp_df = df[(df['Sport'] == sport) & (df['region'] == country)]
    temp_df = temp_df.dropna(subset=["Medal"])

    top = temp_df['Name'].value_counts().reset_index().head(5).merge(df, left_on="Name", right_on="Name", how="left")[
        ["Name", "count"]].drop_duplicates()
    top.rename(columns={"count":"Medal count"},inplace=True)
    return top


def age_vs_medal(df):
    # age vs medal type
    athelete_df = df.drop_duplicates(subset=['Name', 'region'])

    # frequency graph

    #x axis is the age
    #y axis is the frequency-distribution
    x1 = athelete_df['Age'].dropna()
    x2 = athelete_df[athelete_df['Medal'] == 'Gold']['Age'].dropna() #selects the age group where there are gold medalists
    x3 = athelete_df[athelete_df['Medal'] == "Silver"]["Age"].dropna()
    x4 = athelete_df[athelete_df['Medal'] == "Bronze"]["Age"].dropna()
    return x1,x2,x3,x4

def age_vs_sport(df):

    sport_list = ['Basketball',
                  'Judo',
                  'Football',
                  'Tug-Of-War',
                  'Athletics',
                  'Swimming',
                  'Badminton',
                  'Sailing',
                  'Gymnastics',
                  'Art Competitions',
                  'Handball',
                  'Weightlifting',
                  'Wrestling',
                  'Water Polo',
                  'Hockey',
                  'Rowing',
                  'Fencing',
                  'Shooting',
                  'Boxing',
                  'Taekwondo',
                  'Cycling',
                  'Diving',
                  'Canoeing',
                  'Tennis',
                  'Golf',
                  'Softball',
                  'Archery',
                  'Volleyball',
                  'Synchronized Swimming',
                  'Table Tennis',
                  'Baseball',
                  'Rhythmic Gymnastics',
                  'Rugby Sevens',
                  'Beach Volleyball',
                  'Triathlon',
                  'Rugby',
                  'Polo',
                  'Ice Hockey']

    x = []
    name = []
    athelete_df = df.drop_duplicates(subset=['Name', 'region'])

    for sport in sport_list:
        temp_df = athelete_df[athelete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == "Gold"]['Age'].dropna())
        name.append(sport)
    return x,name


#scatter plot for age height weight gender medal
def scatter(df,sport):
    athelete_df=df.drop_duplicates(subset=['Name', 'region'])
    if sport!="Overall":
       athelete_df = athelete_df[athelete_df['Sport'] == sport]
    # age vs weight vs height vs medalists vs gender (female=x, male=.)

    athelete_df["Medal"].fillna("No medal", inplace=True)

    return athelete_df


def gender_plot(df,sport):
    # gender plot
    athelete_df=df.drop_duplicates(subset=['Name', 'region'])
    if sport != "Overall":

        athelete_df = athelete_df[athelete_df['Sport'] == sport]



    female = athelete_df[athelete_df['Sex'] == "F"].groupby('Year').count()['Name'].reset_index()
    male = athelete_df[athelete_df['Sex'] == "M"].groupby('Year').count()['Name'].reset_index()
    final = male.merge(female, on="Year")
    final.rename(columns={"Name_x": "Male", "Name_y": "Female"}, inplace=True)
    final.fillna(0,inplace=True)
    return final













