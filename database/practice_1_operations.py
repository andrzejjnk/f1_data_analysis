import pandas as pd
import numpy as np
from typing import List
from sqlalchemy.sql import text
from insert_data_to_db import Session
from database.db_tables import Practice1Rec
from utils.race_weekends_order import race_orders


def get_all_practice1_data() -> pd.DataFrame:
    with Session() as session:
        try:
            query = text('SELECT * FROM public."Practice1"')
            practice1_records = session.execute(query).fetchall()
            columns = Practice1Rec.__table__.columns.keys()
            records_as_dicts = [dict(zip(columns, record)) for record in practice1_records]
            df = pd.DataFrame(records_as_dicts)
            df['Position'] = df['Position'].replace({0: 'Not Classified', -1: 'DQ'})
            return df

        except Exception as e:
            session.rollback()
            print(f"Cannot fetch the data from database {e}")


def get_practice1_data_data_race_year(country: str, year: int) -> pd.DataFrame:
    if all(isinstance(arg, (str, int)) for arg in (country, year)):
        with Session() as session:
            try:
                query = text('SELECT * FROM public."Practice1" WHERE "Country" = :country AND "Year" = :year')
                values ={
                            'country': country, 
                            'year': year
                        }
                practice1_records = session.execute(query, values).fetchall()
                columns = Practice1Rec.__table__.columns.keys()
                records_as_dicts = [dict(zip(columns, record)) for record in practice1_records]
                df = pd.DataFrame(records_as_dicts)
                df['Position'] = df['Position'].replace({0: 'Not Classified', -1: 'DQ'})
                custom_sort = {'Not Classified': 100, 'DQ': 101}
                df_sorted = df.sort_values(by='Position', key=lambda x: x.map(custom_sort).fillna(x))
                return df_sorted

            except Exception as e:
                session.rollback()
                print(f"Cannot fetch the data from database {e}")


def get_drivers_per_year_from_practice1_data(year: int) -> pd.DataFrame:
    if isinstance(year, int):
        with Session() as session:
            try:
                query = text('SELECT public."Practice1"."Driver" FROM public."Practice1" WHERE "Year" = :year')
                values ={
                            'year': year,
                        }
                practice1_records = session.execute(query, values).fetchall()
                drivers_list = []
                for record in practice1_records:
                    driver_dict = {"Driver": record[0]}
                    drivers_list.append(driver_dict)
                drivers = pd.DataFrame(drivers_list)
                unique_drivers_df = drivers.drop_duplicates()
                
                return unique_drivers_df

            except Exception as e:
                session.rollback()
                print(f"Cannot fetch the data from database {e}")


def get_driver_results_per_year_practice1_data(year: int, driver: str) -> pd.DataFrame:
    if all(isinstance(arg, (str, int)) for arg in (driver, year)):
        with Session() as session:
            try:
                query = text('SELECT * FROM public."Practice1" WHERE "Driver" = :driver AND "Year" = :year')
                values ={
                            'driver': driver,
                            'year': year
                        }
                practice1_records = session.execute(query, values).fetchall()
                columns = Practice1Rec.__table__.columns.keys()
                records_as_dicts = [dict(zip(columns, record)) for record in practice1_records]
                df = pd.DataFrame(records_as_dicts)
                race_order = race_orders[year]

                df['Position'] = df['Position'].replace({0: 'Not Classified', -1: 'DQ'})
                custom_sort = {'Not Classified': 100, 'DQ': 101}
                df_sorted = df.sort_values(by='Position', key=lambda x: x.map(custom_sort).fillna(x))

                df_ordered = pd.DataFrame()
                for _, practice1_name in race_order.items():
                    practice1_data = df_sorted[df_sorted['Country'] == practice1_name]
                    df_ordered = pd.concat([df_ordered, practice1_data])
                
                return df_ordered.reset_index(drop=True)

            except Exception as e:
                session.rollback()
                print(f"Cannot fetch the data from database {e}")


# print(get_all_practice1_data())
# print(get_practice1_data_data_race_year('Austria', 2023))
# print(get_drivers_per_year_from_practice1_data(2022))
# print(get_driver_results_per_year_practice1_data(2024, 'Max Verstappen VER'))