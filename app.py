import os
import pandas as pd
import dash_bootstrap_components as dbc
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import plotly.express as px

# Excel validation
excel_file = 'Data_base_soccer_teams.xlsx'

if not os.path.exists(excel_file):
    raise FileNotFoundError(f"File '{excel_file}' not found. Please upload it to the root directory.")

# load and preparing data
df = pd.read_excel(excel_file)

def prepare_data(df):
    def pivot_aspect(aspect):
        position_aspect = df.groupby(['position', aspect])['name'].count().reset_index()
        pivot = position_aspect.pivot_table(index='position', columns=aspect, values='name').reset_index()
        pivot = pivot.fillna(0)
        expected_cols = ['very high', 'high', 'medium', 'low']
        for col in expected_cols:
            if col not in pivot.columns:
                pivot[col] = 0
        pivot['personality_aspect'] = aspect
        return pivot[['position', 'very high', 'high', 'medium', 'low', 'personality_aspect']]

    df_openness = pivot_aspect('openness')
    df_conscientiousness = pivot_aspect('conscientiousness')
    df_extraversion = pivot_aspect('extraversion')
    df_agreeableness = pivot_aspect('agreeableness')
    
    df_neuroticism = df.groupby(['position','neuroticism'])['name'].count().reset_index()
    pivot_neuro = df_neuroticism.pivot_table(index='position', columns='neuroticism', values='name').reset_index().fillna(0)
    for col in ['very high', 'high', 'medium', 'low']:
        if col not in pivot_neuro.columns:
            pivot_neuro[col] = 0
    pivot_neuro['personality_aspect'] = 'neuroticism'
    df_neuro = pivot_neuro[['position', 'very high', 'high', 'medium', 'low', 'personality_aspect']]

    df_final = pd.concat([df_openness, df_conscientiousness, df_extraversion, df_agreeableness, df_neuro])
    df_final = df_final.rename(columns={"very high": "very_high"})
    return df_final

df_final = prepare_data(df)

# Initialize app
external_stylesheets = [dbc.themes.BOOTSTRAP]
app = Dash(__name__, external_stylesheets=external_stylesheets)
aspects = df_final['personality_aspect'].unique()

# layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H2('Personalities Score Dashboard',
                        style={'textAlign': 'center', 'color': "#0A0A0A", 'marginBottom': '20px'}), width=12)
    ]),
    dbc.Row([
        dbc.Col([
            html.Label("Pick a personality aspect"),
            dcc.RadioItems(
                id='aspect-ratio',
                options=[{'label': aspect.title(), 'value': aspect} for aspect in aspects],
                value=aspects[0],
                inline=True
            )
        ], width=12)
    ], className="mb-4"),
    dbc.Row([
        dbc.Col([
            dash_table.DataTable(
                id='custom-table',
                page_size=10,
                style_table={'overflowX': 'auto', 'height': '400px', 'overflowY': 'auto'},
                style_cell={'textAlign': 'center'},
                style_data={'height': '40px', 'lineHeight': '40px'},
                style_header={'height': '50px', 'lineHeight': '50px', 'fontWeight': 'bold', 'backgroundColor': '#f8f9fa'}
            )
        ], width=6, style={'minHeight': '450px'}),
        dbc.Col([
            html.Div([
                dcc.Graph(id='custom-graph', style={'height': '400px'})
            ], style={'height': '100%'})
        ], width=6, style={'minHeight': '450px'})
    ])
], fluid=True, style={'backgroundColor': '#F9F9F9', 'padding': '20px'})

# callback
@app.callback(
    [Output('custom-table', 'data'),
     Output('custom-table', 'columns'),
     Output('custom-graph', 'figure')],
    [Input('aspect-ratio', 'value')]
)
def update_content(picked_aspect):
    df_filtered = df_final[df_final['personality_aspect'] == picked_aspect]
    data = df_filtered.to_dict('records')
    columns = [{"name": i, "id": i} for i in df_filtered.columns]

    df_melted = df_filtered.melt(
        id_vars=['position', 'personality_aspect'],
        value_vars=['very_high', 'high', 'medium', 'low'],
        var_name='level',
        value_name='value'
    )

    df_melted['total'] = df_melted.groupby(['position', 'personality_aspect'])['value'].transform('sum')
    df_melted['proportion'] = df_melted['value'] / df_melted['total']
    order_df = df_melted[df_melted['level'] == 'very_high'].copy()
    order_df = order_df.sort_values(by='proportion', ascending=False)
    ordered_positions = order_df['position'].tolist()

    fig = px.bar(
        df_melted,
        x='position',
        y='proportion',
        color='level',
        barmode='stack',
        text='value',
        title=f'Distribution of relevance for {picked_aspect.title()} by position',
        labels={'position': 'Position', 'proportion': 'Proportion', 'level': 'Nivel'},
        category_orders={'position': ordered_positions}
    )

    fig.update_layout(yaxis_tickformat=".0%", yaxis_title='Percentage')

    return data, columns, fig

# run
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8050))
    app.run_server(host='0.0.0.0', port=port, debug=False)