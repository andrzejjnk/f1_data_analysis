import pandas as pd


def merge_race_and_sprint_data(race_df, sprint_df) -> pd.DataFrame:
    merged_df: pd.DataFrame = pd.DataFrame()
    race_df_cols = list(race_df.columns)
    sprint_df_cols = list(sprint_df.columns)

    for column in race_df_cols[ :3]:
        merged_df[column] = race_df[column]

    merged_df['Race Points'] = race_df['Points']
    merged_df['Sprint Points'] = sprint_df['Points']

    for column in race_df_cols[3: ]:
        merged_df[column] = race_df[column]

    merged_df['Points'] = race_df['Points'] + sprint_df['Points']
    merged_df.rename(columns = {'Points':'Total Points'}, inplace = True)

    for column in race_df_cols[3: ]:
        if column in sprint_df_cols:
            merged_df[column] = race_df[column] + sprint_df[column]
    merged_df = merged_df.fillna(0)

    return merged_df
