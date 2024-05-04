import os
import pandas as pd
from typing import Dict
from sqlalchemy import MetaData, Table
from sqlalchemy.orm import sessionmaker


from database.db_tables import Base, engine, YearRec, DriverRec, FastestLapsRec, PitStopSummaryRec, Practice1Rec, Practice2Rec, Practice3Rec, QualifyingRec, RaceResultRec, SprintGridRec, SprintQualifyingRec, SprintResultRec, StartingGridRec

# paths to csv files with data
path_drivers = 'data/drivers.csv'
paths_fastest_laps = {2022: "data/2022/fastest_laps/", 2023: "data/2023/fastest_laps/", 2024: "data/2024/fastest_laps/"} 
paths_pit_stop_summary = {2022: "data/2022/pit_stop_summary/", 2023: "data/2023/pit_stop_summary/", 2024: "data/2024/pit_stop_summary/"} 
paths_practice_1 = {2022: "data/2022/practice_1/", 2023: "data/2023/practice_1/", 2024: "data/2024/practice_1/"} 
paths_practice_2 = {2022: "data/2022/practice_2/", 2023: "data/2023/practice_2/", 2024: "data/2024/practice_2/"} 
paths_practice_3= {2022: "data/2022/practice_3/", 2023: "data/2023/practice_3/", 2024: "data/2024/practice_3/"} 
paths_qualifying = {2022: "data/2022/qualifying/", 2023: "data/2023/qualifying/", 2024: "data/2024/qualifying/"} 
paths_race_result = {2022: "data/2022/race_result/", 2023: "data/2023/race_result/", 2024: "data/2024/race_result/"} 
paths_sprint_grid = {2022: "data/2022/sprint_grid/", 2023: "data/2023/sprint_grid/", 2024: "data/2024/sprint_grid/"} 
paths_sprint_qualifying = {2023: "data/2023/sprint_qualifying/", 2024: "data/2024/sprint_qualifying/"} 
paths_sprint_results = {2022: "data/2022/sprint_results/", 2023: "data/2023/sprint_results/", 2024: "data/2024/sprint_results/"} 
paths_starting_grid = {2022: "data/2022/starting_grid/", 2023: "data/2023/starting_grid/", 2024: "data/2024/starting_grid/"} 

# create session 
Session = sessionmaker(bind=engine)

# drop all existing tables in the database 
def drop_all_tables(engine) -> None:
    with Session() as session:
        try:
            metadata = MetaData()
            metadata.reflect(bind=engine)
            
            for table_name in reversed(metadata.sorted_tables):
                table = Table(table_name, metadata)
                table.drop(engine)
            session.commit()

        except Exception as e:
            session.rollback()
            print(f"Cannot clear all tables in the database: {e}")


# clear all existing tables in the database
def clear_all_tables(engine) -> None:
    with Session() as session:
        try:
            metadata = MetaData()
            # read the current database structure 
            metadata.reflect(bind=engine)

            for table_name in metadata.tables.keys():
                current_table = Table(table_name, metadata, autoload=True)
                session.execute(current_table.delete())

            session.commit()

        except Exception as e:
            session.rollback()
            print(f"Cannot clear all tables in the database: {e}")


# add drivers to the database
def add_drivers(path_drivers) -> None:
    with Session() as session:
        try:
            file = pd.read_csv(path_drivers)
            for _, row in file.iterrows():
                record = DriverRec(
                    DriverNumber = row['No'],
                    Name = row['Driver'],
                    Nationality = row['Nationality']
                )
                session.add(record)
            session.commit()

        except Exception as e:
            session.rollback()
            print(f"Cannot insert data to the database: {e}")


# add years to the database
def add_year_records() -> None:
    with Session() as session:
        try:
            years = [2022, 2023, 2024]
            for year in years:
                record = YearRec(
                    Year = year
                )
                session.add(record)

            session.commit()

        except Exception as e:
            session.rollback()
            print(f"Cannot insert data to the database: {e}")


# add data about fastest laps to the database
def add_fastest_laps_records(paths: Dict[int, str]) -> None:
    with Session() as session:
        try:
            for year, path in paths.items():
                files = os.listdir(path)
                for file in files:
                    fastest_laps_data = pd.read_csv(f"{path}/{file}")
                    
                    fastest_laps_data.fillna("-", inplace=True)
                    # Not classified is being replaced by "0" because sqlalchemy not allows to store Integer and String data in a single column
                    fastest_laps_data.replace("NC", 0, inplace=True)
                    country = os.path.splitext(file)[0]

                    for _, row in fastest_laps_data.iterrows():
                        record = FastestLapsRec(
                            Year=year,
                            Country=country,
                            Position=row['Pos'],
                            DriverNumber=row['No'],
                            Driver=row['Driver'],
                            Car = row['Car'],
                            Lap = row['Lap'],
                            TimeOfDay = row['Time of day'],
                            Time = row['Time'].replace('.', ':'),
                            AvgSpeed = row['Avg Speed']
                        )
                        
                        session.add(record)

                    session.commit()
        
        except Exception as e:
            session.rollback()
            print(f"Cannot insert data to the database: {e}")


# add data about pit stops to the database
def add_pitstopsummary_records(paths: Dict[int, str]) -> None:
    with Session() as session:
        try:
            for year, path in paths.items():
                files = os.listdir(path)
                for file in files:
                    pitstop_data = pd.read_csv(f"{path}/{file}")
                    
                    pitstop_data.fillna("-", inplace=True)
                    country = os.path.splitext(file)[0]

                    for _, row in pitstop_data.iterrows():
                        record = PitStopSummaryRec(
                            Year=year,
                            Country=country,
                            Stop=row['Stops'],
                            DriverNumber=row['No'],
                            Driver=row['Driver'],
                            Car = row['Car'],
                            Lap = row['Lap'],
                            TimeOfDay = row['Time of day'],
                            Time = row['Time'],
                            Total = row['Total']
                        )
                        
                        session.add(record)

                    session.commit()
        
        except Exception as e:
            session.rollback()
            print(f"Cannot insert data to the database: {e}")


# add data about practice 1 (FP1) to the database
def add_practice1_records(paths: Dict[int, str]) -> None:
    with Session() as session:
        try:
            for year, path in paths.items():
                files = os.listdir(path)
                for file in files:
                    practice1 = pd.read_csv(f"{path}/{file}")
                    
                    practice1.fillna("-", inplace=True)
                    practice1.replace("NC", 0, inplace=True)
                    country = os.path.splitext(file)[0]

                    for _, row in practice1.iterrows():
                        record = Practice1Rec(
                            Year=year,
                            Country=country,
                            Position=row['Pos'],
                            DriverNumber=row['No'],
                            Driver=row['Driver'],
                            Car = row['Car'],
                            Time = row['Time'].replace('.', ':'),
                            Gap = row['Gap'],
                            Laps = row['Laps']
                        )
                        
                        session.add(record)

                    session.commit()
        
        except Exception as e:
            session.rollback()
            print(f"Cannot insert data to the database: {e}")


# add data about practice 2 (FP2) to the database
def add_practice2_records(paths: Dict[int, str]) -> None:
    with Session() as session:
        try:
            for year, path in paths.items():
                files = os.listdir(path)
                for file in files:
                    practice2 = pd.read_csv(f"{path}/{file}")
                    
                    practice2.fillna("-", inplace=True)
                    practice2.replace("NC", 0, inplace=True)
                    country = os.path.splitext(file)[0]

                    for _, row in practice2.iterrows():
                        record = Practice2Rec(
                            Year=year,
                            Country=country,
                            Position=row['Pos'],
                            DriverNumber=row['No'],
                            Driver=row['Driver'],
                            Car = row['Car'],
                            Time = row['Time'].replace('.', ':'),
                            Gap = row['Gap'],
                            Laps = row['Laps']
                        )
                        
                        session.add(record)

                    session.commit()
        
        except Exception as e:
            session.rollback()
            print(f"Cannot insert data to the database: {e}")


# add data about practice 3 (FP3) to the database
def add_practice3_records(paths: Dict[int, str]) -> None:
    with Session() as session:
        try:
            for year, path in paths.items():
                files = os.listdir(path)
                for file in files:
                    practice3 = pd.read_csv(f"{path}/{file}")
                    
                    practice3.fillna("-", inplace=True)
                    practice3.replace("NC", 0, inplace=True)
                    country = os.path.splitext(file)[0]

                    for _, row in practice3.iterrows():
                        record = Practice3Rec(
                            Year=year,
                            Country=country,
                            Position=row['Pos'],
                            DriverNumber=row['No'],
                            Driver=row['Driver'],
                            Car = row['Car'],
                            Time = row['Time'].replace('.', ':'),
                            Gap = row['Gap'],
                            Laps = row['Laps']
                        )
                        
                        session.add(record)

                    session.commit()
        
        except Exception as e:
            session.rollback()
            print(f"Cannot insert data to the database: {e}")


# add data from qualifications to the database
def add_qualification_records(paths: Dict[int, str]) -> None:
    with Session() as session:
        try:
            for year, path in paths.items():
                files = os.listdir(path)
                for file in files:
                    qualifying_data = pd.read_csv(f"{path}/{file}")
                    
                    qualifying_data.fillna("-", inplace=True)
                    # Not classified is being replaced by "0" because sqlalchemy not allows to store Integer and String data in a single column
                    qualifying_data.replace("NC", 0, inplace=True)
                    qualifying_data.replace(',', ':', inplace=True)
                    country = os.path.splitext(file)[0]

                    for _, row in qualifying_data.iterrows():
                        record = QualifyingRec(
                            Year=year,
                            Country=country,
                            Position=row['Pos'],
                            DriverNumber=row['No'],
                            Driver=row['Driver'],
                            Car=row['Car'],
                            Q1=row['Q1'].replace('.', ':'),
                            Q2=row['Q2'].replace('.', ':'),
                            Q3=row['Q3'].replace('.', ':'),
                            Laps=row['Laps']
                        )
                        
                        session.add(record)

                    session.commit()
        
        except Exception as e:
            session.rollback()
            print(f"Cannot insert data to the database: {e}")


# add race results data to the database
def add_raceresult_records(paths: Dict[int, str]) -> None:
    with Session() as session:
        try:
            for year, path in paths.items():
                files = os.listdir(path)
                for file in files:
                    race_result_data = pd.read_csv(f"{path}/{file}")
                    
                    race_result_data.fillna("-", inplace=True)
                    # Not classified is being replaced by "0" and DQ as -1 because sqlalchemy not allows to store Integer and String data in a single column
                    race_result_data.replace("NC", 0, inplace=True)
                    race_result_data.replace("DQ", -1, inplace=True)
                    country = os.path.splitext(file)[0]

                    for _, row in race_result_data.iterrows():
                        record = RaceResultRec(
                            Year=year,
                            Country=country,
                            Position=row['Pos'],
                            DriverNumber=row['No'],
                            Driver=row['Driver'],
                            Car=row['Car'],
                            Laps=row['Laps'],
                            Time=row['Time/Retired'],
                            Points=row['PTS']
                        )
                        
                        session.add(record)

                    session.commit()
        
        except Exception as e:
            session.rollback()
            print(f"Cannot insert data to the database: {e}")


# add data about grid to the sprint to database
def add_sprint_grid_records(paths: Dict[int, str]) -> None:
    with Session() as session:
        try:
            for year, path in paths.items():
                files = os.listdir(path)
                for file in files:
                    sprint_grid_data = pd.read_csv(f"{path}/{file}")
                    # Not classified is being replaced by "0" and DQ as -1 because sqlalchemy not allows to store Integer and String data in a single column
                    sprint_grid_data.fillna("-", inplace=True)
                    sprint_grid_data.replace("NC", 0, inplace=True)
                    sprint_grid_data.replace("DQ", -1, inplace=True)
                    country = os.path.splitext(file)[0]

                    for _, row in sprint_grid_data.iterrows():
                        record = SprintGridRec(
                            Year=year,
                            Country=country,
                            Position=row['Pos'],
                            DriverNumber=row['No'],
                            Driver=row['Driver'],
                            Car=row['Car'],
                            Time=row['Time'].replace('.', ':')
                        )
                        
                        session.add(record)

                    session.commit()
        
        except Exception as e:
            session.rollback()
            print(f"Cannot insert data to the database: {e}")


# add data about qualifications for sprint to the database
def add_sprint_qualification_records(paths: Dict[int, str]) -> None:
    with Session() as session:
        try:
            for year, path in paths.items():
                files = os.listdir(path)
                for file in files:
                    sprint_qualifying_data = pd.read_csv(f"{path}/{file}")
                    
                    sprint_qualifying_data.fillna("-", inplace=True)
                    # Not classified is being replaced by "0" and DQ as -1 because sqlalchemy not allows to store Integer and String data in a single column
                    sprint_qualifying_data.replace("NC", 0, inplace=True)
                    sprint_qualifying_data.replace("DQ", -1, inplace=True)
                    #sprint_qualifying_data.replace(".", ":", inplace=True)
                    country = os.path.splitext(file)[0]

                    for _, row in sprint_qualifying_data.iterrows():
                        record = SprintQualifyingRec(
                            Year=year,
                            Country=country,
                            Position=row['Pos'],
                            DriverNumber=row['No'],
                            Driver=row['Driver'],
                            Car=row['Car'],
                            Q1=row['Q1'].replace('.', ':'),
                            Q2=row['Q2'].replace('.', ':'),
                            Q3=row['Q3'].replace('.', ':'),
                            Laps=row['Laps']
                        )
                        
                        session.add(record)

                    session.commit()
        
        except Exception as e:
            session.rollback()
            print(f"Cannot insert data to the database: {e}")


# add sprint results data to the database
def add_sprint_result_records(paths: Dict[int, str]) -> None:
    with Session() as session:
        try:
            for year, path in paths.items():
                files = os.listdir(path)
                for file in files:
                    sprint_result_data = pd.read_csv(f"{path}/{file}")
                    
                    sprint_result_data.fillna("-", inplace=True)
                    # Not classified is being replaced by "0" and DQ as -1 because sqlalchemy not allows to store Integer and String data in a single column
                    sprint_result_data.replace("NC", 0, inplace=True)
                    sprint_result_data.replace("DQ", -1, inplace=True)
                    country = os.path.splitext(file)[0]

                    for _, row in sprint_result_data.iterrows():
                        record = SprintResultRec(
                            Year=year,
                            Country=country,
                            Position=row['Pos'],
                            DriverNumber=row['No'],
                            Driver=row['Driver'],
                            Car=row['Car'],
                            Laps=row['Laps'],
                            Time=row['Time/Retired'],
                            Points=row['PTS']
                        )
                        
                        session.add(record)

                    session.commit()
        
        except Exception as e:
            session.rollback()
            print(f"Cannot insert data to the database: {e}")


# add data about starting grid to race to the database
def add_starting_grid_records(paths: Dict[int, str]) -> None:
    with Session() as session:
        try:
            for year, path in paths.items():
                files = os.listdir(path)
                for file in files:
                    starting_grid_data = pd.read_csv(f"{path}/{file}")
                    # Not classified is being replaced by "0" and DQ as -1 because sqlalchemy not allows to store Integer and String data in a single column
                    starting_grid_data.fillna("-", inplace=True)
                    starting_grid_data.replace("NC", 0, inplace=True)
                    starting_grid_data.replace("DQ", -1, inplace=True)
                    country = os.path.splitext(file)[0]

                    for _, row in starting_grid_data.iterrows():
                        record = StartingGridRec(
                            Year=year,
                            Country=country,
                            Position=row['Pos'],
                            DriverNumber=row['No'],
                            Driver=row['Driver'],
                            Car=row['Car'],
                            Time=row['Time'].replace('.', ':'),
                        )
                        
                        session.add(record)

                    session.commit()
        
        except Exception as e:
            print(f"country: {country}")
            session.rollback()
            print(f"Cannot insert data to the database: {e}")


# init database and clear the data
def init_database(engine) -> None:
    try:
        drop_all_tables(engine)
        Base.metadata.create_all(engine)
        clear_all_tables(engine)
        print("Database successfully initialized!")

    except Exception as e:
        print("Cannot init database: {e}")


# insert to the database data from csv files to appropriate tables in database
def insert_data_to_database() -> None:
    try:
        add_drivers(path_drivers)
        add_year_records()
        add_fastest_laps_records(paths_fastest_laps)
        add_pitstopsummary_records(paths_pit_stop_summary)
        add_practice1_records(paths_practice_1)
        add_practice2_records(paths_practice_2)
        add_practice3_records(paths_practice_3)
        add_qualification_records(paths_qualifying)
        add_raceresult_records(paths_race_result)
        add_sprint_grid_records(paths_sprint_grid)
        add_sprint_qualification_records(paths_sprint_qualifying)
        add_sprint_result_records(paths_sprint_results)
        add_starting_grid_records(paths_starting_grid)
        print("Data successfully inserted into database!")

    except Exception as e:
        print("Cannot insert data into database: {e}")


if __name__=="__main__":
    init_database(engine)
    insert_data_to_database()


# drop_all_tables(engine)
# Base.metadata.create_all(engine)
# clear_all_tables(engine)
# add_drivers(path_drivers)
# add_year_records()
# add_fastest_laps_records(paths_fastest_laps)
# add_pitstopsummary_records(paths_pit_stop_summary)
# add_practice1_records(paths_practice_1)
# add_practice2_records(paths_practice_2)
# add_practice3_records(paths_practice_3)
# add_qualification_records(paths_qualifying)
# add_raceresult_records(paths_race_result)
# add_sprint_grid_records(paths_sprint_grid)
# add_sprint_qualification_records(paths_sprint_qualifying)
# add_sprint_result_records(paths_sprint_results)
# add_starting_grid_records(paths_starting_grid)

