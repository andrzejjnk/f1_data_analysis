import pandas as pd
import numpy as np
from sqlalchemy.sql import text
from insert_data_to_db import Session
from database.db_tables import RaceResultRec
from utils.race_weekends_order import race_orders


def get_race_result_data_race_year(country: str, year: int) -> pd.DataFrame:
    if all(isinstance(arg, (str, int)) for arg in (country, year)):
        with Session() as session:
            try:
                query = text('SELECT * FROM public."RaceResults" WHERE "Country" = :country AND "Year" = :year')
                values ={
                            'country': country, 
                            'year': year
                        }
                race_records = session.execute(query, values).fetchall()
                columns = RaceResultRec.__table__.columns.keys()
                records_as_dicts = [dict(zip(columns, record)) for record in race_records]
                df = pd.DataFrame(records_as_dicts)
                df['Position'] = df['Position'].replace({0: 'Not Classified', -1: 'DQ'})
                custom_sort = {'Not Classified': 100, 'DQ': 101}
                df_sorted = df.sort_values(by='Position', key=lambda x: x.map(custom_sort).fillna(x))
                return df_sorted

            except Exception as e:
                session.rollback()
                print(f"Cannot fetch the data from database {e}")


def get_all_race_result_data() -> pd.DataFrame:
    with Session() as session:
        try:
            query = text('SELECT * FROM public."RaceResults"')
            race_records = session.execute(query).fetchall()
            columns = RaceResultRec.__table__.columns.keys()
            records_as_dicts = [dict(zip(columns, record)) for record in race_records]
            df = pd.DataFrame(records_as_dicts)
            df['Position'] = df['Position'].replace({0: 'Not Classified', -1: 'DQ'})
            return df

        except Exception as e:
            session.rollback()
            print(f"Cannot fetch the data from database {e}")


def get_all_race_results_per_year(year: int) -> pd.DataFrame:
    if isinstance(year, int):
        with Session() as session:
            try:
                query = text('SELECT * FROM public."RaceResults" WHERE "Year" = :year')
                values ={
                            'year': year
                        }
                race_records = session.execute(query, values).fetchall()
                columns = RaceResultRec.__table__.columns.keys()
                records_as_dicts = [dict(zip(columns, record)) for record in race_records]
                df = pd.DataFrame(records_as_dicts)
                df['Position'] = df['Position'].replace({0: 'Not Classified', -1: 'DQ'})
                return df

            except Exception as e:
                session.rollback()
                print(f"Cannot fetch the data from database {e}")


def get_race_results_for_country(country: str) -> pd.DataFrame:
    if isinstance(country, str):
        with Session() as session:
            try:
                query = text('SELECT * FROM public."RaceResults" WHERE "Country" = :country')
                values ={
                            'country': country
                        }
                race_records = session.execute(query, values).fetchall()
                columns = RaceResultRec.__table__.columns.keys()
                records_as_dicts = [dict(zip(columns, record)) for record in race_records]
                df = pd.DataFrame(records_as_dicts)
                df['Position'] = df['Position'].replace({0: 'Not Classified', -1: 'DQ'})
                df_sorted = df.sort_values(by='Year', ascending=True)
                return df_sorted

            except Exception as e:
                session.rollback()
                print(f"Cannot fetch the data from database {e}")


def get_driver_points_per_season_with_race_results(year: int) -> pd.DataFrame:
    if not isinstance(year, int):
        raise ValueError("Year must be an integer.")

    with Session() as session:
        try:
            query = text('SELECT * FROM public."RaceResults" WHERE "Year" = :year')
            values = {'year': year}
            race_records = session.execute(query, values).fetchall()
            
            columns = RaceResultRec.__table__.columns.keys()
            df_race_results = pd.DataFrame([dict(zip(columns, record)) for record in race_records])
            df_driver_points = df_race_results.groupby(['Driver', 'Car'])['Points'].sum().reset_index()
            pivot_table = pd.pivot_table(df_race_results, values='Points', index='Driver', columns='Country', aggfunc=np.sum, fill_value=0)
            race_order = race_orders[year]
            pivot_table_ordered = pivot_table[[race_order[i] for i in range(1, len(race_order) + 1)]]
            df_merged = pd.merge(df_driver_points, pivot_table_ordered, on='Driver')
            df_merged_sorted = df_merged.sort_values(by='Points', ascending=False)
            return df_merged_sorted

        except Exception as e:
            session.rollback()
            print(f"Cannot fetch the data from database: {e}")


def get_driver_results_per_year(year: int, driver: str) -> pd.DataFrame:
    if all(isinstance(arg, (str, int)) for arg in (driver, year)):
        with Session() as session:
            try:
                query = text('SELECT * FROM public."RaceResults" WHERE "Driver" = :driver AND "Year" = :year')
                values ={
                            'driver': driver,
                            'year': year
                        }
                race_records = session.execute(query, values).fetchall()
                columns = RaceResultRec.__table__.columns.keys()
                records_as_dicts = [dict(zip(columns, record)) for record in race_records]
                df = pd.DataFrame(records_as_dicts)
                race_order = race_orders[year]

                df['Position'] = df['Position'].replace({0: 'Not Classified', -1: 'DQ'})
                custom_sort = {'Not Classified': 100, 'DQ': 101}
                df_sorted = df.sort_values(by='Position', key=lambda x: x.map(custom_sort).fillna(x))

                df_ordered = pd.DataFrame()
                for race_num, race_name in race_order.items():
                    race_data = df_sorted[df_sorted['Country'] == race_name]
                    df_ordered = pd.concat([df_ordered, race_data])
                
                return df_ordered.reset_index(drop=True)

            except Exception as e:
                session.rollback()
                print(f"Cannot fetch the data from database {e}")


def get_driver_results_per_country(country: int, driver: str) -> None | pd.DataFrame:
    if all(isinstance(arg, (str, str)) for arg in (driver, country)):
        with Session() as session:
            try:
                query = text('SELECT * FROM public."RaceResults" WHERE "Driver" = :driver AND "Country" = :country')
                values ={
                            'driver': driver,
                            'country': country
                        }
                race_records = session.execute(query, values).fetchall()
                columns = RaceResultRec.__table__.columns.keys()
                records_as_dicts = [dict(zip(columns, record)) for record in race_records]
                df = pd.DataFrame(records_as_dicts)
                df['Position'] = df['Position'].replace({0: 'Not Classified', -1: 'DQ'})
                df_sorted = df.sort_values(by='Year', ascending=True)
                return df_sorted

            except Exception as e:
                session.rollback()
                print(f"Cannot fetch the data from database {e}")
                return None


def get_drivers_per_year_from_races(year: int) -> pd.DataFrame:
    if isinstance(year, int):
        with Session() as session:
            try:
                query = text('SELECT public."RaceResults"."Driver" FROM public."RaceResults" WHERE "Year" = :year')
                values ={
                            'year': year,
                        }
                race_records = session.execute(query, values).fetchall()
                drivers_list = []
                for record in race_records:
                    driver_dict = {"Driver": record[0]}
                    drivers_list.append(driver_dict)
                drivers = pd.DataFrame(drivers_list)
                unique_drivers_df = drivers.drop_duplicates()
                
                return unique_drivers_df

            except Exception as e:
                session.rollback()
                print(f"Cannot fetch the data from database {e}")

def get_countries_per_year(year: int) -> pd.DataFrame:
    if isinstance(year, int):
        with Session() as session:
            try:
                query = text('SELECT public."RaceResults"."Country" FROM public."RaceResults" WHERE "Year" = :year')
                values ={
                            'year': year,
                        }
                race_records = session.execute(query, values).fetchall()
                countries_list = []
                for record in race_records:
                    country_dict = {"Country": record[0]}
                    countries_list.append(country_dict)
                countries = pd.DataFrame(countries_list)
                unique_countries_df = countries.drop_duplicates()
                
                return unique_countries_df

            except Exception as e:
                session.rollback()
                print(f"Cannot fetch the data from database {e}")


# race_results_year_country = get_race_result_data_race_year('Austria', 2022)
# all_race_results_all_years_all_countries = get_all_race_result_data()
# all_race_results_per_specified_year = get_all_race_results_per_year(2024)
# race_results_all_years_specified_country = get_race_results_for_country('Saudi Arabia')
# driver_points_with_race_results_specified_year = get_driver_points_per_season_with_race_results(2022)
# race_results_specified_driver_specified_year = get_driver_results_per_year(2022, 'Max Verstappen VER')
# race_results_specified_country_specified_driver = get_driver_results_per_country('Bahrain', 'Max Verstappen VER')
# drivers_participated_in_races_in_specified_year = get_drivers_per_year_from_races(2024)
# print(race_results_specified_driver_specified_year)
# print(get_countries_per_year(2023))

# print(get_driver_results_per_country('Bahrain', 'Sebastian Vettel VET'))
# print(get_driver_results_per_country('Bahrain', 'Max Verstappen VER'))