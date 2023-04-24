import pandas as pd

teams = pd.read_csv('data/teams.csv')
teams_geo = pd.read_html('https://en.wikipedia.org/wiki/National_Basketball_Association#Teams')[3]
teams_geo = teams_geo.iloc[:, [0, 1, 5]]
teams_geo = teams_geo.drop(15)
teams_geo['lat'] = teams_geo.iloc[:, -1].apply(lambda x: x.split(' / ')[-1].split(' ')[0][:-2])
teams_geo['lng'] = teams_geo.iloc[:, -2].apply(lambda x: x.split(' / ')[-1].split(' ')[1][:-2])
teams_geo.columns = teams_geo.columns.droplevel(1)
teams = pd.merge(teams, teams_geo, left_on='full_name', right_on='Team')
teams = teams.drop(columns=['Coordinates', 'Team'])
x = [[team['abbreviation'] for _, team in teams.iterrows() if team['Division'] == division] for division in teams['Division'].unique()]

print(x)
