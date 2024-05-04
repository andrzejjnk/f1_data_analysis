from typing import List
import plotly.graph_objs as go
from utils.colours import colour_for_teams
from database.standings_operations import merge_race_and_sprint_data
from database.race_results_operations import get_driver_points_per_season_with_race_results
from database.sprints_operations import get_driver_points_per_season_with_sprint_results


def plot_drivers_points_specified_year_standings(year: int, drivers_to_compare: List[str] = None) -> go.Figure:
    if not isinstance(year, int):
        raise ValueError("Year must be an integer.")
    
    race_df = get_driver_points_per_season_with_race_results(year)
    sprint_df = get_driver_points_per_season_with_sprint_results(year)
    df = merge_race_and_sprint_data(race_df, sprint_df)

    if drivers_to_compare is not None and isinstance(drivers_to_compare, list):
        drivers = drivers_to_compare
    else:
        drivers = df['Driver'].unique()
    races = df.columns[5:]

    fig = go.Figure()

    max_points = 0
    for driver in drivers:
        driver_data = df[df['Driver'] == driver]
        team = driver_data['Car'].values[0]
        team_color = colour_for_teams.get(team, (0, 0, 0))
        driver_points = driver_data.iloc[:, 5:].cumsum(axis=1)
        fig.add_trace(go.Scatter(x=races, 
                                 y=driver_points.values.flatten(),
                                 mode='lines+markers',
                                 name=driver,
                                 marker=dict(color=f'rgb({team_color[0]}, {team_color[1]}, {team_color[2]})')))
        
    max_points = max(max_points, driver_points.values.flatten()[-1])

    fig.update_layout(xaxis_title='Race Weekend',
                      yaxis_title='Total Points',
                      title='Total Points from races after specified race weekends',
                      xaxis=dict(tickangle=45),
                      legend=dict(orientation='v', yanchor='top', y=0.8, xanchor='right', x=1.2),
                      margin=dict(l=50, r=50, t=50, b=50),
                      grid=dict(rows=True, columns=True),
                      width=1650,
                      height=900,
                      legend_tracegroupgap=0)
    
    return fig