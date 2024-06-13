import pandas as pd
import numpy as np
from sqlalchemy.sql import text
from insert_data_to_db import Session
from database.db_tables import RaceResultRec
from utils.race_weekends_order import race_orders
from sqlalchemy.exc import SQLAlchemyError


def get_race_result_data_race_year(country: str, year: int) -> pd.DataFrame:
    if all(isinstance(arg, (str, int)) for arg in (country, year)):
        with Session() as session:
            try:
                race_records = session.query(RaceResultRec).filter_by(Country=country, Year=year).all()
                records_as_dicts = [record.__dict__ for record in race_records]
                for record in records_as_dicts:
                    record.pop('_sa_instance_state', None)
                df = pd.DataFrame(records_as_dicts)
                df['Position'] = df['Position'].replace({0: 'Not Classified', -1: 'DQ'})
                custom_sort = {'Not Classified': 100, 'DQ': 101}
                df_sorted = df.sort_values(by='Position', key=lambda x: x.map(custom_sort).fillna(x))
                return df_sorted
            except SQLAlchemyError as e:
                session.rollback()
                print(f"Cannot fetch the data from database {e}")


def get_all_race_result_data() -> pd.DataFrame:
    with Session() as session:
        try:
            race_records = session.query(RaceResultRec).all()
            records_as_dicts = [record.__dict__ for record in race_records]
            for record in records_as_dicts:
                record.pop('_sa_instance_state', None)
            df = pd.DataFrame(records_as_dicts)
            df['Position'] = df['Position'].replace({0: 'Not Classified', -1: 'DQ'})
            return df
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Cannot fetch the data from database {e}")


def get_all_race_results_per_year(year: int) -> pd.DataFrame:
    if isinstance(year, int):
        with Session() as session:
            try:
                race_records = session.query(RaceResultRec).filter_by(Year=year).all()
                records_as_dicts = [record.__dict__ for record in race_records]
                for record in records_as_dicts:
                    record.pop('_sa_instance_state', None)
                df = pd.DataFrame(records_as_dicts)
                df['Position'] = df['Position'].replace({0: 'Not Classified', -1: 'DQ'})
                return df
            except SQLAlchemyError as e:
                session.rollback()
                print(f"Cannot fetch the data from database {e}")


def get_race_results_for_country(country: str) -> pd.DataFrame:
    if isinstance(country, str):
        with Session() as session:
            try:
                race_records = session.query(RaceResultRec).filter_by(Country=country).all()
                records_as_dicts = [record.__dict__ for record in race_records]
                for record in records_as_dicts:
                    record.pop('_sa_instance_state', None)
                df = pd.DataFrame(records_as_dicts)
                df['Position'] = df['Position'].replace({0: 'Not Classified', -1: 'DQ'})
                df_sorted = df.sort_values(by='Year', ascending=True)
                return df_sorted
            except SQLAlchemyError as e:
                session.rollback()
                print(f"Cannot fetch the data from database {e}")


def get_driver_points_per_season_with_race_results(year: int) -> pd.DataFrame:
    if not isinstance(year, int):
        raise ValueError("Year must be an integer.")

    with Session() as session:
        try:
            race_records = session.query(RaceResultRec).filter_by(Year=year).all()
            records_as_dicts = [record.__dict__ for record in race_records]
            for record in records_as_dicts:
                record.pop('_sa_instance_state', None)
            df_race_results = pd.DataFrame(records_as_dicts)
            df_driver_points = df_race_results.groupby(['Driver', 'Car'])['Points'].sum().reset_index()
            pivot_table = pd.pivot_table(df_race_results, values='Points', index='Driver', columns='Country', aggfunc=np.sum, fill_value=0)
            race_order = race_orders[year]
            pivot_table_ordered = pivot_table[[race_order[i] for i in range(1, len(race_order) + 1)]]
            df_merged = pd.merge(df_driver_points, pivot_table_ordered, on='Driver')
            df_merged_sorted = df_merged.sort_values(by='Points', ascending=False)
            return df_merged_sorted
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Cannot fetch the data from database: {e}")


def get_driver_results_per_year(year: int, driver: str) -> pd.DataFrame:
    if all(isinstance(arg, (str, int)) for arg in (driver, year)):
        with Session() as session:
            try:
                race_records = session.query(RaceResultRec).filter_by(Driver=driver, Year=year).all()
                records_as_dicts = [record.__dict__ for record in race_records]
                for record in records_as_dicts:
                    record.pop('_sa_instance_state', None)
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
            except SQLAlchemyError as e:
                session.rollback()
                print(f"Cannot fetch the data from database {e}")


def get_driver_results_per_country(country: str, driver: str) -> None | pd.DataFrame:
    if all(isinstance(arg, (str, str)) for arg in (driver, country)):
        with Session() as session:
            try:
                race_records = session.query(RaceResultRec).filter_by(Driver=driver, Country=country).all()
                records_as_dicts = [record.__dict__ for record in race_records]
                for record in records_as_dicts:
                    record.pop('_sa_instance_state', None)
                df = pd.DataFrame(records_as_dicts)
                df['Position'] = df['Position'].replace({0: 'Not Classified', -1: 'DQ'})
                df_sorted = df.sort_values(by='Year', ascending=True)
                return df_sorted
            except SQLAlchemyError as e:
                session.rollback()
                print(f"Cannot fetch the data from database {e}")
                return None


def get_drivers_per_year_from_races(year: int) -> pd.DataFrame:
    if isinstance(year, int):
        with Session() as session:
            try:
                race_records = session.query(RaceResultRec.Driver).filter_by(Year=year).distinct().all()
                drivers_list = [{"Driver": record[0]} for record in race_records]
                drivers = pd.DataFrame(drivers_list)
                return drivers
            except SQLAlchemyError as e:
                session.rollback()
                print(f"Cannot fetch the data from database {e}")


def get_countries_per_year(year: int) -> pd.DataFrame:
    if isinstance(year, int):
        with Session() as session:
            try:
                race_records = session.query(RaceResultRec.Country).filter_by(Year=year).distinct().all()
                countries_list = [{"Country": record[0]} for record in race_records]
                countries = pd.DataFrame(countries_list)
                return countries
            except SQLAlchemyError as e:
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