import numpy as np
import pandas as pd


def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(
        subset=['discipline_title', 'event_title', 'event_gender', 'medal_type', 'participant_type', 'country_name',
                'city', 'year'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['country_name'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['year'] == int(year)]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['year'] == int(year)) & (medal_df['country_name'] == country)]
    if flag == 1:
        x = temp_df.groupby('year').sum()[['GOLD', 'SILVER', 'BRONZE']].sort_values('year').reset_index()
    else:
        x = temp_df.groupby('country_name').sum()[['GOLD', 'SILVER', 'BRONZE']].sort_values('GOLD',
                                                                                            ascending=False).reset_index()
    x['total'] = x['GOLD'] + x['SILVER'] + x['BRONZE']

    x['GOLD'] = x['GOLD'].astype('int')
    x['SILVER'] = x['SILVER'].astype('int')
    x['BRONZE'] = x['BRONZE'].astype('int')
    x['total'] = x['total'].astype('int')

    return x

def medal_tally(df):
    medal_tally = df.drop_duplicates(
        subset=['discipline_title', 'event_title', 'event_gender', 'medal_type', 'participant_type', 'country_name',
                'city', 'year'])
    medal_tally = medal_tally.groupby('country_name').sum()[['GOLD', 'SILVER', 'BRONZE']].sort_values('GOLD',
                                                                                                      ascending=False).reset_index()
    medal_tally['total'] = medal_tally['GOLD'] + medal_tally['SILVER'] + medal_tally['BRONZE']

    medal_tally['GOLD'] = medal_tally['GOLD'].astype('int')
    medal_tally['SILVER'] = medal_tally['SILVER'].astype('int')
    medal_tally['BRONZE'] = medal_tally['BRONZE'].astype('int')
    medal_tally['total'] = medal_tally['total'].astype('int')

    return medal_tally

def country_year_list(df):
    years = df['year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = df['country_name'].unique().tolist()
    country.insert(0, 'Overall')

    return years,country

def data_over_time(df,col):

    nations_over_time = df.drop_duplicates(['year', col])['year'].value_counts().reset_index().sort_values('year')
    nations_over_time.rename(columns={'year': 'Edition', 'count': col}, inplace=True)
    return nations_over_time

def most_succesful(df,sport):
    temp_df=df.dropna(subset='athlete_full_name')
    if sport!='Overall':
        temp_df=temp_df[temp_df['discipline_title']==sport]
    x= temp_df['athlete_full_name'].value_counts().reset_index().head(15).merge(df,left_on='athlete_full_name',right_on='athlete_full_name',how='left')[['athlete_full_name','count','discipline_title','country_name']].drop_duplicates('athlete_full_name')
    x.rename(columns={'athlete_full_name_x':'Name','count':'Medals'},inplace=True)
    return x;

def yearwise_medal_tally(df,country):
    temp_df = df
    temp_df.drop_duplicates(
        subset=['discipline_title', 'event_title', 'event_gender', 'medal_type', 'participant_type', 'country_name',
                'year'], inplace=True)
    new_df = temp_df[temp_df['country_name'] == country]
    final_df = new_df.groupby('year').count()['medal_type'].reset_index()
    return final_df

def country_event_heatmap(df,country):
    temp_df = df
    temp_df.drop_duplicates(
        subset=['discipline_title', 'event_title', 'event_gender', 'medal_type', 'participant_type', 'country_name',
                'year'], inplace=True)
    new_df = temp_df[temp_df['country_name'] == country]
    pt=new_df.pivot_table(index='discipline_title',columns='year',values='medal_type',aggfunc='count').fillna(0)
    return pt

def most_succesful_countrywise(df,country):
    temp_df=df.dropna(subset='athlete_full_name')
    temp_df=temp_df[temp_df['country_name']==country]
    x= temp_df['athlete_full_name'].value_counts().reset_index().head(10).merge(df,left_on='athlete_full_name',right_on='athlete_full_name',how='left')[['athlete_full_name','count','discipline_title']].drop_duplicates('athlete_full_name')
    x.rename(columns={'athlete_full_name_x':'Name','count':'Medals'},inplace=True)
    return x;

def men_vs_women_mixed(df):
    men = df[df['event_gender'] == 'Men'].groupby('year').count()['athlete_full_name'].reset_index()
    women = df[df['event_gender'] == 'Women'].groupby('year').count()['athlete_full_name'].reset_index()
    mixed = df[df['event_gender'] == 'Mixed'].groupby('year').count()['athlete_full_name'].reset_index()
    final = men.merge((women), on='year')
    final = final.merge((mixed), on='year')
    final.rename(columns={'athlete_full_name_x': 'Male', 'athlete_full_name_y': 'Female', 'athlete_full_name': 'Mixed'},
                 inplace=True)
    final.fillna(0, inplace=True)
    return final