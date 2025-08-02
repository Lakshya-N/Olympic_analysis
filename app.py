import streamlit as st
import pandas as pd
import preprocessor
import helper
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
df=pd.read_csv('athlete_events.csv')
region_df=pd.read_csv('noc_regions.csv')


df=preprocessor.preprocess(df,region_df)


user_menu=st.sidebar.radio(
    "Select an option",
    ("Medal Tally","Overall Analysis","Country-wise Analysis","Athlete wise Analysis")
)

# to show a dataframe or a tabular data in a nice formatted,scrollable table on streamlit



st.sidebar.title("Olympics Analysis")
#if the user clicks the medal_tally

if user_menu=="Medal Tally":
    st.sidebar.header('Medal Tally')
    year,country=helper.country_year_list(df)

    selected_year=st.sidebar.selectbox("Select year",year)
    selected_country=st.sidebar.selectbox("Select country",country)


    medal_tally=helper.fetch_medal_tally(df,selected_year,selected_country)

    if selected_year=="Overall" and selected_country=="Overall":
        st.title("Overall Tally")
    elif selected_year =="Overall" and selected_country!="Overall":
        st.title("Overall Tally for Country:"+str(selected_country))
    elif selected_year!="Overall" and selected_country=="Overall":
        st.title("Tally for the year:"+str(selected_year))
    else:
        st.title(selected_country+"Tally for the Year:"+str(selected_year))


    st.dataframe(medal_tally)

#Overall analysis
if user_menu=="Overall Analysis":
    st.title("Top Statistics")
    edition=df['Year'].unique().shape[0]-1
    cities= df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events= df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    col1,col2,col3=st.columns(3)
    with col1:
        st.header("Editions")
        st.title(edition)
    with col2:
        st.header("Cities")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Athletes")
        st.title(athletes)
    with col3:
        st.header("Nations")
        st.title(nations)

    #graph of participation
    nations_over_time=helper.data_over_time(df,'region')
    fig=px.line(nations_over_time,x="Edition",y="region")
    st.title("Participating nations over time")
    st.plotly_chart(fig)


   #graph for the number of events conducted over years
    nations_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(nations_over_time, x="Edition", y="Event")
    st.title("Events over time")
    st.plotly_chart(fig)

    #number of athelets over time
    nations_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(nations_over_time, x="Edition", y="Name")
    st.title("Atheletes over time")
    st.plotly_chart(fig)




    st.title("No. of Events over time (Every sport analysis")

    fig,ax=plt.subplots(figsize=(20,20))


    x=df.drop_duplicates(['Year','Sport','Event'])
    ax=sns.heatmap(x.pivot_table(index="Sport", columns="Year", values="Event", aggfunc="count").fillna(0).astype(int),
                annot=True)
    st.pyplot(fig)
    #top players


    st.title("Most successfull Athletes")

    years,sports=helper.year_and_sports(df)
    selected_sports=st.selectbox("Select sport",sports)
    x=helper.most_successfull(df,selected_sports)
    st.table(x)


#Country-wise analysis
if user_menu=="Country-wise Analysis":
    country=df['region'].unique().tolist()


    selected_country=st.sidebar.selectbox("Select Country",country)

    #line plot
    tally=helper.year_wise_medal_tally(df,selected_country)
    fig = px.line(tally, x='Year', y='Medal')
    st.title("Medal tally over the years  for "+selected_country)
    st.plotly_chart(fig)


    #heat map
    st.title(selected_country+" 's Heat map")
    pt=helper.country_event_heatmap(df,selected_country)
    fig,ax=plt.subplots(figsize=(20,20))
    ax=sns.heatmap(pt,annot=True)
    st.pyplot(fig)


    #country and sports based top atheletes of all time

    sports=df['Sport'].unique().tolist()
    sports.insert(0,"Overall")
    st.title("Top 10 Players of "+selected_country)
    selected_sport=st.selectbox("Select sport",sports)
    st.title(selected_sport)
    top=helper.top_athletes(df,selected_country,selected_sport)
    st.table(top)


#if Athelete-wise analysis

if user_menu=="Athlete wise Analysis":
    #age vs wins of players
    st.title("Distribution of Age")
    x1,x2,x3,x4=helper.age_vs_medal(df)
    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                             show_hist=False, show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.plotly_chart(fig)


    #age vs sports

    st.title("Age distribution with respect to sports(gold medalist only)")



    x,name=helper.age_vs_sport(df)
    fig = ff.create_distplot(x, name,show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)



    #scatter plot
    st.title("Height vs Weight ")
    sports = df['Sport'].unique().tolist()
    sports.insert(0, "Overall")
    selected_sport2=st.selectbox("Select sport",sports,key="Sport_select_2")
    temp_df=helper.scatter(df,selected_sport2)
    fig,ax=plt.subplots()

    ax=sns.scatterplot(x='Weight', y="Height", hue='Medal', style='Sex', data=temp_df,s=100)

    st.pyplot(fig)


    #gender plot
    st.title("Gender wise participation over the years")
    sports = df['Sport'].unique().tolist()
    sports.insert(0, "Overall")
    selected_sport= st.selectbox("Select sport", sports,key="Sport_select_3")
    final=helper.gender_plot(df,selected_sport)

    fig=px.line(final,x="Year",y=["Male","Female"])
    st.plotly_chart(fig)








    




