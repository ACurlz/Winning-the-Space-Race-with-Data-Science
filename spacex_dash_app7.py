# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'},
            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
        ],
        value='ALL',
        placeholder="Select a Launch Site",
        searchable=True,
        style={'width': '50%'}
    ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                # Task 2: Callback function to update success-pie-chart based on selected site dropdown
@app.callback(
    Output('success-pie-chart', 'figure'),
    [Input('site-dropdown', 'value')]
)
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        # Total successful launches count for all sites
        total_success = spacex_df[spacex_df['class'] == 1]['class'].count()
        total_failed = spacex_df[spacex_df['class'] == 0]['class'].count()
        labels = ['Success', 'Failed']
        values = [total_success, total_failed]
        title = 'Total Successful Launches Count for All Sites'
    else:
        # Success vs. Failed counts for the selected site
        site_data = spacex_df[spacex_df['Launch Site'] == selected_site]
        success = site_data[site_data['class'] == 1]['class'].count()
        failed = site_data[site_data['class'] == 0]['class'].count()
        labels = ['Success', 'Failed']
        values = [success, failed]
        title = f'Success vs. Failed Counts for {selected_site}'

    # Create pie chart figure
    fig = px.pie(names=labels, values=values, title=title)
    return fig
    html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
    dcc.RangeSlider(
        id='payload-slider',
        min=0,
        max=10000,
        step=1000,
        marks={i: str(i) for i in range(0, 10001, 1000)},
        value=[0, 10000]
    ),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])# Task 4: Callback function to update success-payload-scatter-chart based on selected site and payload range
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def update_scatter_chart(selected_site, selected_payload_range):
    if selected_site == 'ALL':
        # Scatter plot for all sites
        scatter_data = spacex_df[(spacex_df['Payload Mass (kg)'] >= selected_payload_range[0]) & 
                                  (spacex_df['Payload Mass (kg)'] <= selected_payload_range[1])]
        fig = px.scatter(scatter_data, x='Payload Mass (kg)', y='class',
                         color='Booster Version Category', title='Payload vs. Outcome for All Sites',
                         labels={'class': 'Outcome', 'Payload Mass (kg)': 'Payload Mass (kg)'})
    else:
        # Scatter plot for the selected site
        site_data = spacex_df[spacex_df['Launch Site'] == selected_site]
        scatter_data = site_data[(site_data['Payload Mass (kg)'] >= selected_payload_range[0]) & 
                                 (site_data['Payload Mass (kg)'] <= selected_payload_range[1])]
        fig = px.scatter(scatter_data, x='Payload Mass (kg)', y='class',
                         color='Booster Version Category', title=f'Payload vs. Outcome for {selected_site}',
                         labels={'class': 'Outcome', 'Payload Mass (kg)': 'Payload Mass (kg)'})
    
    return fig


# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output


# Run the app
if __name__ == '__main__':
    app.run_server()
