import numpy as np


def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    elif year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    elif year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    else:
        temp_df = medal_df[(medal_df['Year'] == int(year)) & (medal_df['region'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year')[['Gold', 'Silver', 'Bronze']].sum().sort_index().reset_index()
    else:
        x = temp_df.groupby('region')[['Gold', 'Silver', 'Bronze']].sum().sort_values('Gold', ascending=False).reset_index()

    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']

    x['Gold'] = x['Gold'].astype(int)
    x['Silver'] = x['Silver'].astype(int)
    x['Bronze'] = x['Bronze'].astype(int)
    x['total'] = x['total'].astype(int)

    return x


def country_year_list(df):
    years = df['Year'].dropna().unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    countries = np.unique(df['region'].dropna().values).tolist()
    countries.sort()
    countries.insert(0, 'Overall')

    return years, countries


def data_over_time(df, col):
    data = df.drop_duplicates(subset=['Year', col])
    count_df = data['Year'].value_counts().reset_index()
    count_df.columns = ['Edition', col]
    count_df = count_df.sort_values('Edition')
    return count_df


def most_successful(df, sport):
    temp_df = df.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    x = temp_df['Name'].value_counts().reset_index().head(15)
    x.columns = ['Name', 'Medals']
    x = x.merge(df, on='Name', how='left')
    x = x[['Name', 'Medals', 'Sport', 'region']].drop_duplicates('Name')
    return x


def yearwise_medal_tally(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])

    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year')['Medal'].count().reset_index()

    return final_df


def country_event_heatmap(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])

    new_df = temp_df[temp_df['region'] == country]
    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)

    return pt


def most_successful_countrywise(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['region'] == country]

    x = temp_df['Name'].value_counts().reset_index().head(10)
    x.columns = ['Name', 'Medals']
    x = x.merge(df, on='Name', how='left')
    x = x[['Name', 'Medals', 'Sport']].drop_duplicates('Name')
    return x


def weight_v_height(df, sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'] = athlete_df['Medal'].fillna('No Medal')
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df


def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year')['Name'].count().reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year')['Name'].count().reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)
    final.fillna(0, inplace=True)
    return final
