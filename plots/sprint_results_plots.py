from typing import List
import plotly.graph_objs as go
from utils.colours import colour_for_teams
from database.sprints_operations import get_driver_points_per_season_with_sprint_results, get_driver_results_per_year_sprints, get_driver_results_per_country, get_drivers_per_year_from_sprints


def plot_drivers_points_specified_year_sprints(year: int, drivers_to_compare: List[str] = None) -> go.Figure:
    if not isinstance(year, int):
        raise ValueError("Year must be an integer.")
    
    df = get_driver_points_per_season_with_sprint_results(year)

    if drivers_to_compare is not None and isinstance(drivers_to_compare, list):
        drivers = drivers_to_compare
    else:
        drivers = df['Driver'].unique()
    races = df.columns[3:]

    fig = go.Figure()

    max_points = 0
    for driver in drivers:
        driver_data = df[df['Driver'] == driver]
        team = driver_data['Car'].values[0]
        team_color = colour_for_teams.get(team, (0, 0, 0))
        driver_points = driver_data.iloc[:, 3:].cumsum(axis=1)
        fig.add_trace(go.Scatter(x=races, 
                                 y=driver_points.values.flatten(),
                                 mode='lines+markers',
                                 name=driver,
                                 marker=dict(color=f'rgb({team_color[0]}, {team_color[1]}, {team_color[2]})')))
        
    max_points = max(max_points, driver_points.values.flatten()[-1])

    fig.update_layout(xaxis_title='Sprint Weekend',
                      yaxis_title='Total Points',
                      title='Total Points from sprints after specified sprint weekends',
                      xaxis=dict(tickangle=45),
                      legend=dict(orientation='v', yanchor='top', y=0.8, xanchor='right', x=1.2),
                      margin=dict(l=50, r=50, t=50, b=50),
                      grid=dict(rows=True, columns=True),
                      width=1650,
                      height=900,
                      legend_tracegroupgap=0)
    
    return fig


def plot_comparision_between_drivers_specified_year_sprints(year: int, drivers_to_compare: List[str] = None) -> go.Figure:
    if not isinstance(year, int):
        raise ValueError("Year must be an integer.")
    
    if drivers_to_compare is None:
        drivers_to_compare = get_drivers_per_year_from_sprints(year)['Driver'].tolist()

    fig = go.Figure()

    max_position = 20

    for driver in drivers_to_compare:
        df = get_driver_results_per_year_sprints(year, driver)
        team = df['Car'].values[0]
        team_color = colour_for_teams.get(team, (0, 0, 0))
        positions = df['Position'].replace({'Not Classified': max_position + 1, 'DQ': max_position + 1}).astype(int)
        fig.add_trace(go.Scatter(x=df['Country'], 
                                 y=positions, 
                                 mode='lines+markers', 
                                 name=driver,
                                 marker=dict(color=f'rgb({team_color[0]}, {team_color[1]}, {team_color[2]})')))

    fig.update_layout(xaxis_title='Sprint Weekend',
                      yaxis_title='Position',
                      title=f'Comparison between drivers in {year}',
                      xaxis=dict(tickangle=45),
                      yaxis=dict(tickmode='array', tickvals=list(range(1, max_position + 2)), ticktext=list(range(1, max_position + 1)) + ['Not Classified/DQ']),
                      legend=dict(orientation='v', yanchor='top', y=0.8, xanchor='right', x=1.2),
                      margin=dict(l=50, r=50, t=50, b=50),
                      grid=dict(rows=True, columns=True),
                      width=1650,
                      height=900,
                      legend_tracegroupgap=0)
    
    return fig


def plot_comparision_between_drivers_specified_country_sprints(country: str, drivers_to_compare: List[str]) -> go.Figure:
    if not isinstance(country, str):
        raise ValueError("Year must be an integer.")
    
    fig = go.Figure()

    max_position = 20

    for driver in drivers_to_compare:
        df = get_driver_results_per_country(country, driver)
        if df is None:
            continue
        team = df['Car'].values[0]
        team_color = colour_for_teams.get(team, (0, 0, 0))
        positions = df['Position'].replace({'Not Classified': max_position + 1, 'DQ': max_position + 1}).astype(int)
        fig.add_trace(go.Scatter(x=df['Year'], 
                                 y=positions, 
                                 mode='lines+markers', 
                                 name=driver,
                                 marker=dict(color=f'rgb({team_color[0]}, {team_color[1]}, {team_color[2]})')))

    fig.update_layout(xaxis_title='Year',
                      yaxis_title='Position',
                      title=f'Comparision between drivers at {country} Sprint',
                      xaxis=dict(tickangle=45, tickmode='array', tickvals=list(range(2022, 2024+1)), ticktext=list(range(2022, 2024+1))),
                      yaxis=dict(tickmode='array', tickvals=list(range(1, max_position + 2)), ticktext=list(range(1, max_position + 1)) + ['Not Classified/DQ']),
                      legend=dict(orientation='v', yanchor='top', y=0.8, xanchor='right', x=1.2),
                      margin=dict(l=50, r=50, t=50, b=50),
                      grid=dict(rows=True, columns=True),
                      width=1650,
                      height=900,
                      legend_tracegroupgap=0)
    
    return fig