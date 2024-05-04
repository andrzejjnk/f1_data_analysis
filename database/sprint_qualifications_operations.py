import pandas as pd
from sqlalchemy.sql import text
from insert_data_to_db import Session
from database.db_tables import SprintQualifyingRec
from utils.sprint_weekends_order import sprint_orders


def get_all_sprint_qualifications_data() -> pd.DataFrame:
    with Session() as session:
        try:
            query = text('SELECT * FROM public."SprintQualifications"')
            sprint_qualification_records = session.execute(query).fetchall()
            columns = SprintQualifyingRec.__table__.columns.keys()
            records_as_dicts = [dict(zip(columns, record)) for record in sprint_qualification_records]
            df = pd.DataFrame(records_as_dicts)
            df['Position'] = df['Position'].replace({0: 'Not Classified', -1: 'DQ'})
            return df

        except Exception as e:
            session.rollback()
            print(f"Cannot fetch the data from database {e}")


def get_sprint_qualifications_data_sprint_year(country: str, year: int) -> pd.DataFrame:
    if all(isinstance(arg, (str, int)) for arg in (country, year)):
        with Session() as session:
            try:
                query = text('SELECT * FROM public."SprintQualifications" WHERE "Country" = :country AND "Year" = :year')
                values ={
                            'country': country, 
                            'year': year
                        }
                sprint_qualification_records = session.execute(query, values).fetchall()
                columns = SprintQualifyingRec.__table__.columns.keys()
                records_as_dicts = [dict(zip(columns, record)) for record in sprint_qualification_records]
                df = pd.DataFrame(records_as_dicts)
                df['Position'] = df['Position'].replace({0: 'Not Classified', -1: 'DQ'})
                custom_sort = {'Not Classified': 100, 'DQ': 101}
                df_sorted = df.sort_values(by='Position', key=lambda x: x.map(custom_sort).fillna(x))
                return df_sorted

            except Exception as e:
                session.rollback()
                print(f"Cannot fetch the data from database {e}")


def get_drivers_per_year_from_sprint_qualifications(year: int) -> pd.DataFrame:
    if isinstance(year, int):
        with Session() as session:
            try:
                query = text('SELECT public."SprintQualifications"."Driver" FROM public."SprintQualifications" WHERE "Year" = :year')
                values ={
                            'year': year,
                        }
                sprint_qualification_records = session.execute(query, values).fetchall()
                drivers_list = []
                for record in sprint_qualification_records:
                    driver_dict = {"Driver": record[0]}
                    drivers_list.append(driver_dict)
                drivers = pd.DataFrame(drivers_list)
                unique_drivers_df = drivers.drop_duplicates()
                
                return unique_drivers_df

            except Exception as e:
                session.rollback()
                print(f"Cannot fetch the data from database {e}")


def get_driver_results_per_year_sprint_qualifications(year: int, driver: str) -> pd.DataFrame:
    if all(isinstance(arg, (str, int)) for arg in (driver, year)):
        with Session() as session:
            try:
                query = text('SELECT * FROM public."SprintQualifications" WHERE "Driver" = :driver AND "Year" = :year')
                values ={
                            'driver': driver,
                            'year': year
                        }
                sprint_qualification_records = session.execute(query, values).fetchall()
                columns = SprintQualifyingRec.__table__.columns.keys()
                records_as_dicts = [dict(zip(columns, record)) for record in sprint_qualification_records]
                df = pd.DataFrame(records_as_dicts)
                sprint_order = sprint_orders[year]

                df['Position'] = df['Position'].replace({0: 'Not Classified', -1: 'DQ'})
                custom_sort = {'Not Classified': 100, 'DQ': 101}
                df_sorted = df.sort_values(by='Position', key=lambda x: x.map(custom_sort).fillna(x))

                df_ordered = pd.DataFrame()
                for _, sprint_quali_name in sprint_order.items():
                    sprint_quali_data = df_sorted[df_sorted['Country'] == sprint_quali_name]
                    df_ordered = pd.concat([df_ordered, sprint_quali_data])
                
                return df_ordered.reset_index(drop=True)

            except Exception as e:
                session.rollback()
                print(f"Cannot fetch the data from database {e}")


# print(get_all_sprint_qualifications_data())
# print(get_sprint_qualifications_data_sprint_year('Austria', 2023))
# print(get_drivers_per_year_from_sprint_qualifications(2023))
# print(get_driver_results_per_year_sprint_qualifications(2024, 'Max Verstappen VER'))