import pandas as pd
from sqlalchemy.sql import text
from insert_data_to_db import Session
from database.db_tables import QualifyingRec
from utils.race_weekends_order import race_orders
from sqlalchemy.exc import SQLAlchemyError


def get_all_qualifications_data() -> pd.DataFrame:
    with Session() as session:
        try:
            qualification_records = session.query(QualifyingRec).all()
            records_as_dicts = [record.__dict__ for record in qualification_records]
            for record in records_as_dicts:
                record.pop('_sa_instance_state', None)
            df = pd.DataFrame(records_as_dicts)
            df['Position'] = df['Position'].replace({0: 'Not Classified', -1: 'DQ'})
            return df
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Cannot fetch the data from database {e}")


def get_qualifications_data_race_year(country: str, year: int) -> pd.DataFrame:
    if all(isinstance(arg, (str, int)) for arg in (country, year)):
        with Session() as session:
            try:
                qualification_records = session.query(QualifyingRec).filter_by(Country=country, Year=year).all()
                records_as_dicts = [record.__dict__ for record in qualification_records]
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


def get_drivers_per_year_from_qualifications(year: int) -> pd.DataFrame:
    if isinstance(year, int):
        with Session() as session:
            try:
                qualification_records = session.query(QualifyingRec.Driver).filter_by(Year=year).distinct().all()
                drivers_list = [{"Driver": record[0]} for record in qualification_records]
                drivers = pd.DataFrame(drivers_list)
                return drivers
            except SQLAlchemyError as e:
                session.rollback()
                print(f"Cannot fetch the data from database {e}")


def get_driver_results_per_year_qualifications(year: int, driver: str) -> pd.DataFrame:
    if all(isinstance(arg, (str, int)) for arg in (driver, year)):
        with Session() as session:
            try:
                qualification_records = session.query(QualifyingRec).filter_by(Driver=driver, Year=year).all()
                records_as_dicts = [record.__dict__ for record in qualification_records]
                for record in records_as_dicts:
                    record.pop('_sa_instance_state', None)
                df = pd.DataFrame(records_as_dicts)
                race_order = race_orders.get(year, {})

                df['Position'] = df['Position'].replace({0: 'Not Classified', -1: 'DQ'})
                custom_sort = {'Not Classified': 100, 'DQ': 101}
                df_sorted = df.sort_values(by='Position', key=lambda x: x.map(custom_sort).fillna(x))

                df_ordered = pd.DataFrame()
                for _, quali_name in race_order.items():
                    quali_data = df_sorted[df_sorted['Country'] == quali_name]
                    df_ordered = pd.concat([df_ordered, quali_data])
                
                return df_ordered.reset_index(drop=True)
            except SQLAlchemyError as e:
                session.rollback()
                print(f"Cannot fetch the data from database {e}")


# print(get_all_qualifications_data())
# print(get_qualifications_data_race_year('Austria', 2023))
# print(get_drivers_per_year_from_qualifications(2022))
#print(get_driver_results_per_year_qualifications(2024, 'Max Verstappen VER'))