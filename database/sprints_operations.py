import pandas as pd
import numpy as np
from sqlalchemy.sql import text
from insert_data_to_db import Session
from database.db_tables import SprintResultRec
from utils.sprint_weekends_order import sprint_orders
from sqlalchemy.exc import SQLAlchemyError


def get_sprint_result_data_sprint_year(country: str, year: int) -> pd.DataFrame:
    if all(isinstance(arg, (str, int)) for arg in (country, year)):
        with Session() as session:
            try:
                sprint_records = session.query(SprintResultRec).filter_by(Country=country, Year=year).all()
                records_as_dicts = [record.__dict__ for record in sprint_records]
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


def get_all_sprint_result_data() -> pd.DataFrame:
    with Session() as session:
        try:
            sprint_records = session.query(SprintResultRec).all()
            records_as_dicts = [record.__dict__ for record in sprint_records]
            for record in records_as_dicts:
                record.pop('_sa_instance_state', None)
            df = pd.DataFrame(records_as_dicts)
            df['Position'] = df['Position'].replace({0: 'Not Classified', -1: 'DQ'})
            return df
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Cannot fetch the data from database {e}")


def get_all_sprint_results_per_year(year: int) -> pd.DataFrame:
    if isinstance(year, int):
        with Session() as session:
            try:
                sprint_records = session.query(SprintResultRec).filter_by(Year=year).all()
                records_as_dicts = [record.__dict__ for record in sprint_records]
                for record in records_as_dicts:
                    record.pop('_sa_instance_state', None)
                df = pd.DataFrame(records_as_dicts)
                df['Position'] = df['Position'].replace({0: 'Not Classified', -1: 'DQ'})
                return df
            except SQLAlchemyError as e:
                session.rollback()
                print(f"Cannot fetch the data from database {e}")


def get_sprint_results_for_country(country: str) -> pd.DataFrame:
    if isinstance(country, str):
        with Session() as session:
            try:
                sprint_records = session.query(SprintResultRec).filter_by(Country=country).all()
                records_as_dicts = [record.__dict__ for record in sprint_records]
                for record in records_as_dicts:
                    record.pop('_sa_instance_state', None)
                df = pd.DataFrame(records_as_dicts)
                df['Position'] = df['Position'].replace({0: 'Not Classified', -1: 'DQ'})
                df_sorted = df.sort_values(by='Year', ascending=True)
                return df_sorted
            except SQLAlchemyError as e:
                session.rollback()
                print(f"Cannot fetch the data from database {e}")


def get_driver_points_per_season_with_sprint_results(year: int) -> pd.DataFrame:
    if not isinstance(year, int):
        raise ValueError("Year must be an integer.")

    with Session() as session:
        try:
            sprint_records = session.query(SprintResultRec).filter_by(Year=year).all()
            records_as_dicts = [record.__dict__ for record in sprint_records]
            for record in records_as_dicts:
                record.pop('_sa_instance_state', None)
            df_sprint_results = pd.DataFrame(records_as_dicts)
            df_driver_points = df_sprint_results.groupby(['Driver', 'Car'])['Points'].sum().reset_index()
            pivot_table = pd.pivot_table(df_sprint_results, values='Points', index='Driver', columns='Country', aggfunc=np.sum, fill_value=0)
            sprint_order = sprint_orders[year]
            pivot_table_ordered = pivot_table[[sprint_order[i] for i in range(1, len(sprint_order) + 1)]]
            df_merged = pd.merge(df_driver_points, pivot_table_ordered, on='Driver')
            df_merged_sorted = df_merged.sort_values(by='Points', ascending=False)
            return df_merged_sorted
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Cannot fetch the data from database {e}")


def get_driver_results_per_year_sprints(year: int, driver: str) -> pd.DataFrame:
    if all(isinstance(arg, (str, int)) for arg in (driver, year)):
        with Session() as session:
            try:
                sprint_records = session.query(SprintResultRec).filter_by(Driver=driver, Year=year).all()
                records_as_dicts = [record.__dict__ for record in sprint_records]
                for record in records_as_dicts:
                    record.pop('_sa_instance_state', None)
                df = pd.DataFrame(records_as_dicts)
                sprint_order = sprint_orders[year]

                df['Position'] = df['Position'].replace({0: 'Not Classified', -1: 'DQ'})
                custom_sort = {'Not Classified': 100, 'DQ': 101}
                df_sorted = df.sort_values(by='Position', key=lambda x: x.map(custom_sort).fillna(x))

                df_ordered = pd.DataFrame()
                for _, sprint_name in sprint_order.items():
                    sprint_data = df_sorted[df_sorted['Country'] == sprint_name]
                    df_ordered = pd.concat([df_ordered, sprint_data])
                
                return df_ordered.reset_index(drop=True)
            except SQLAlchemyError as e:
                session.rollback()
                print(f"Cannot fetch the data from database {e}")


def get_driver_results_per_country(country: str, driver: str) -> None | pd.DataFrame:
    if all(isinstance(arg, (str, str)) for arg in (driver, country)):
        with Session() as session:
            try:
                sprint_records = session.query(SprintResultRec).filter_by(Driver=driver, Country=country).all()
                records_as_dicts = [record.__dict__ for record in sprint_records]
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


def get_drivers_per_year_from_sprints(year: int) -> pd.DataFrame:
    if isinstance(year, int):
        with Session() as session:
            try:
                sprint_records = session.query(SprintResultRec.Driver).filter_by(Year=year).distinct().all()
                drivers_list = [{"Driver": record[0]} for record in sprint_records]
                drivers = pd.DataFrame(drivers_list)
                return drivers
            except SQLAlchemyError as e:
                session.rollback()
                print(f"Cannot fetch the data from database {e}")


def get_countries_per_year(year: int) -> pd.DataFrame:
    if isinstance(year, int):
        with Session() as session:
            try:
                sprint_records = session.query(SprintResultRec.Country).filter_by(Year=year).distinct().all()
                countries_list = [{"Country": record[0]} for record in sprint_records]
                countries = pd.DataFrame(countries_list)
                return countries
            except SQLAlchemyError as e:
                session.rollback()
                print(f"Cannot fetch the data from database {e}")


# sprint_results_year_country = get_sprint_result_data_sprint_year('Austria', 2022)
# all_sprint_results_all_years_all_countries = get_all_sprint_result_data()
# all_sprint_results_per_specified_year = get_all_sprint_results_per_year(2024)
# sprint_results_all_years_specified_country = get_sprint_results_for_country('Austria')
# driver_points_with_sprint_results_specified_year = get_driver_points_per_season_with_sprint_results(2022)
# sprint_results_specified_driver_specified_year = get_driver_results_per_year_sprints(2022, 'Max Verstappen VER')
# sprint_results_specified_country_specified_driver = get_driver_results_per_country('Imola', 'Max Verstappen VER')
# drivers_participated_in_sprints_in_specified_year = get_drivers_per_year_from_sprints(2024)
# print(drivers_participated_in_sprints_in_specified_year)