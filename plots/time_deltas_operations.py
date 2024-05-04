import pandas as pd 
import plotly.graph_objects as go
from utils.colours import colour_for_teams


def time_difference(fastest_lap: str, lap_time_co_compare: str) -> float:
    if not isinstance(fastest_lap, str) or  not isinstance(lap_time_co_compare, str):
        raise ValueError("fastest_lap and lap_time_co_compare must be a str.")
    
    def time_to_seconds(time_str: str) -> float:
        if not isinstance(time_str, str):
            raise ValueError("time_str must be a str.")
        minutes, seconds, milliseconds = map(float, time_str.split(':'))
        return minutes * 60 + seconds + milliseconds / 1000

    time1_seconds = time_to_seconds(fastest_lap)
    time2_seconds = time_to_seconds(lap_time_co_compare)

    difference = f'{abs(time1_seconds - time2_seconds):.3f}'
    difference = float(difference)
    
    return difference


def find_min_value_in_column(col: pd.DataFrame) -> str:
    min = "999:999:999"
    for _, value in col.items():
        if value != '-' and value != 'DNF':
            if value < min:
                min = value
    return min


def calculate_time_delta(df: pd.DataFrame) -> pd.DataFrame:
    if not isinstance(df, pd.DataFrame):
        raise ValueError("df must be a pd.DataFrame.")

    qualifying_sessions = [col for col in df.columns if col.startswith('Q')]

    for session in qualifying_sessions:
        differences = []
        fastest_time = find_min_value_in_column(df[session])
        for _, lap_time in df[session].items():
            if lap_time != '-' and lap_time != 'DNF' and lap_time != 'DNS':
                difference = time_difference(fastest_time, lap_time)
                differences.append(difference)
            else:
                differences.append(lap_time)

        df[session + '_Gaps'] = differences
    
    return df


def plot_time_gap_per_session(df: pd.DataFrame, session: str) -> go.Figure:
    if not isinstance(df, pd.DataFrame) or not isinstance(session, str):
        raise ValueError("df must be a pd.DataFrame and session must be a str.")
    
    session_data = df[df[session + '_Gaps'] != '-'].copy()
    session_data[session + '_Gaps'] = pd.to_numeric(session_data[session + '_Gaps'], errors='coerce')
    session_data = session_data.sort_values(by=session + '_Gaps', ascending=True)
    session_data[session + '_Gaps'].fillna('DNF', inplace=True)
    
    if session == 'Q1':
        session_data = session_data.head(20)
    elif session == 'Q2':
        session_data = session_data.head(15)
    elif session == 'Q3':
        session_data = session_data.head(10)

    Country = session_data['Country'].unique()[0]
    fig = go.Figure()

    for _, row in session_data.iterrows():
        team_color = colour_for_teams.get(row['Car'], (0, 0, 0))
        fig.add_trace(go.Bar(x=[row['Driver']], y=[row[session + '_Gaps']], text=[row[session + '_Gaps']],
                             marker_color=f'rgb({team_color[0]}, {team_color[1]}, {team_color[2]})',
                             name=row['Driver']))

    fig.update_traces(texttemplate='%{text}', textposition='outside')
    fig.update_yaxes(title_text='Time Gap (seconds)')
    fig.update_xaxes(title_text='Driver')

    fig.update_layout(title=f'Time Gap to Leader in {Country} {session} session',
                    xaxis=dict(tickangle=45),
                    legend=dict(orientation='v', yanchor='top', y=0.8, xanchor='right', x=1.2),
                    margin=dict(l=50, r=50, t=50, b=50),
                    grid=dict(rows=True, columns=True),
                    width=1650,
                    height=900,
                    legend_tracegroupgap=0)

    return fig


def plot_time_gap_practice_session(df: pd.DataFrame, session: str) -> go.Figure:
    if not isinstance(df, pd.DataFrame) or not isinstance(session, str):
        raise ValueError("df must be a pd.DataFrame and session must be a str.")
    
    df_copy = df.copy()
    df_copy['Gap'] = df_copy['Gap'].str.replace('+', '', regex=False).str.replace('s', '', regex=False).replace('-', '0').astype(float)


    df_sorted = df_copy.sort_values(by='Gap', ascending=True)
    df_sorted = df_copy.sort_values(by='Position', ascending=True)
    df_sorted.loc[df_sorted['Time'].isin(['-', 'DNF', 'DNS']), 'Gap'] = 'DNF'
    Country = df_sorted['Country'].unique()[0]

    fig = go.Figure()

    for _, row in df_sorted.iterrows():
        team_color = colour_for_teams.get(row['Car'], (0, 0, 0))
        # if row['Gap'] == 'DNF':
        #     continue
        fig.add_trace(go.Bar(x=[row['Driver']], y=[row['Gap']], text=[row['Gap']],
                                marker_color=f'rgb({team_color[0]}, {team_color[1]}, {team_color[2]})',
                                name=row['Driver']))

    fig.update_traces(texttemplate='%{text}', textposition='outside')
    fig.update_yaxes(title_text='Time Gap (seconds)')
    fig.update_xaxes(title_text='Driver')

    fig.update_layout(title=f'Time Gap to Leader in {Country} {session} session',
                    xaxis=dict(tickangle=45),
                    legend=dict(orientation='v', yanchor='top', y=0.8, xanchor='right', x=1.2),
                    margin=dict(l=50, r=50, t=50, b=50),
                    grid=dict(rows=True, columns=True),
                    width=1650,
                    height=900,
                    legend_tracegroupgap=0)

    #fig.show()
    return fig

