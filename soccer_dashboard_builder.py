import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from dash import Dash, html, dash_table

df = pd.read_excel('C:/Users/kmilo/Documents/Data_analyst_projects/7_Soccer_dashboard/football_analysis_dashboard/Data_base_soccer_teams.xlsx')


# 1_Analysis of openness aspect

position_openness = df.groupby(['position','openness'])['name'].count()

position_openness = position_openness.reset_index()
position_openness = position_openness.sort_values(by = ['position'], ascending = False)
pivot_openness = position_openness.pivot_table(index = 'position', columns = 'openness', values = 'name')
pivot_openness = pivot_openness.reset_index()
pivot_openness = pivot_openness.fillna(0)
pivot_openness = pivot_openness[['position', 'very high', 'high', 'medium', 'low']]

pivot_openness.plot(kind = 'bar', x = 'position', ylabel = 'Number of players', title = 'Level of openness by position')

pivot_openness['personality_aspect'] = 'openness'

# 2_Analysis of conscientiousness aspect

position_conscientiousness = df.groupby(['position','conscientiousness'])['name'].count()
position_conscientiousness = position_conscientiousness.reset_index()
position_conscientiousness = position_conscientiousness.sort_values(by = ['position'], ascending = False)
pivot_conscientiousness = position_conscientiousness.pivot_table(index = 'position', columns = 'conscientiousness', values = 'name')
pivot_conscientiousness = pivot_conscientiousness.reset_index()
pivot_conscientiousness = pivot_conscientiousness.fillna(0)
pivot_conscientiousness = pivot_conscientiousness[['position', 'very high', 'high', 'medium', 'low']]

pivot_conscientiousness.plot(kind = 'bar', x = 'position', ylabel = 'Number of players', title =  'Level of conscientiousness by position')

pivot_conscientiousness['personality_aspect'] = 'conscientiousness'

# 3_Analysis of extraversion aspect

position_extraversion = df.groupby(['position','extraversion'])['name'].count()
position_extraversion = position_extraversion.reset_index()
position_extraversion = position_extraversion.sort_values(by = ['position'], ascending = False)
pivot_extraversion = position_extraversion.pivot_table(index = 'position', columns = 'extraversion', values = 'name')
pivot_extraversion = pivot_extraversion.reset_index()
pivot_extraversion = pivot_extraversion.fillna(0)
pivot_extraversion = pivot_extraversion[['position', 'very high', 'high', 'medium', 'low']]

pivot_extraversion.plot(kind = 'bar', x = 'position', ylabel = 'Number of players', title =  'Level of extraversion by position')

pivot_extraversion['personality_aspect'] = 'extraversion'


# 4_Analysis of agreeableness aspect

position_agreeableness = df.groupby(['position','agreeableness'])['name'].count()
position_agreeableness = position_agreeableness.reset_index()
position_agreeableness = position_agreeableness.sort_values(by = ['position'], ascending = False)
pivot_agreeableness = position_agreeableness.pivot_table(index = 'position', columns = 'agreeableness', values = 'name')
pivot_agreeableness = pivot_agreeableness.reset_index()
pivot_agreeableness = pivot_agreeableness.fillna(0)
pivot_agreeableness = pivot_agreeableness[['position', 'very high', 'high', 'medium', 'low']]

pivot_agreeableness.plot(kind = 'bar', x = 'position', ylabel = 'Number of players', title =  'Level of agreeableness by position')

pivot_agreeableness['personality_aspect'] =  'agreeableness'

#_Analysis of neuroticism aspect

position_neuroticism = df.groupby(['position','neuroticism'])['name'].count()
position_neuroticism = position_neuroticism.reset_index()
position_neuroticism = position_neuroticism.sort_values(by = ['position','name'], ascending = False)
pivot_neuroticism = position_neuroticism.pivot_table(index = 'position', columns = 'neuroticism', values = 'name')
pivot_neuroticism = pivot_neuroticism.reset_index()
pivot_neuroticism = pivot_neuroticism.fillna(0)
pivot_neuroticism = pivot_neuroticism[['position', 'high', 'medium', 'low']]

pivot_neuroticism.plot(kind = 'bar', x = 'position', ylabel = 'Number of players', title =  'Level of neuroticism by position')

pivot_neuroticism['personality_aspect'] =  'neuroticism'

# final table 

df_final = pd.concat([pivot_openness, pivot_conscientiousness, pivot_extraversion, pivot_agreeableness,pivot_neuroticism])

df_final = df_final.fillna(0)
df_final = df_final[['position','personality_aspect', 'very high', 'high', 'medium', 'low']]
df_final = df_final.rename(columns = {"very high":"very_high"})

# initialize app

app = Dash()

# app layout

app.layout = [html.Div(children= 'Soccer personalities table'), dash_table.DataTable(data=df_final.to_dict('records'),columns = [{"name": "Position", "id": "position"},
            {"name": "Personality Aspect", "id": "personality_aspect"},
            {"name": "Very High", "id": "very_high"},
            {"name": "High", "id": "high"},
            {"name": "Medium", "id": "medium"},
            {"name": "Low", "id": "low"}], page_size=10)]
# run the app

if __name__ == '__main__':

    app.run(debug=True)