import pandas as pd



def preprocess(df,region_df):

    #filtering the summer olympics data alone
    df=df[df['Season']=='Summer']

    #merge with region df

    df=df.merge(region_df,on='NOC',how='left')

    # dropping the duplicate rows
    df.drop_duplicates(inplace=True)

    #one hot encoding - categorical text to machine understandable numbers to analyse and process

    df=pd.concat([df,pd.get_dummies(df['Medal'])],axis=1)

    return df