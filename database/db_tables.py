from sqlalchemy import Column, Integer, String, Float
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import UniqueConstraint, ForeignKey


# connection to the database and create engine
db_string = "postgresql://postgres:password@localhost:5432/postgres"
Base = declarative_base()
engine = create_engine(db_string)


# Declaration of database tables
class YearRec(Base):
    __tablename__="Years"
    Year = Column(Integer, primary_key=True)

    fastestlaps = relationship("FastestLapsRec", back_populates="year_fastestlaps")
    pitstopssummary = relationship("PitStopSummaryRec", back_populates="year_pitstopssummary")
    practice1 = relationship("Practice1Rec", back_populates="year_practice1")
    practice2 = relationship("Practice2Rec", back_populates="year_practice2")
    practice3 = relationship("Practice3Rec", back_populates="year_practice3")
    qualifications = relationship("QualifyingRec", back_populates="year_qualifications")
    raceresults = relationship("RaceResultRec", back_populates="year_raceresults")
    sprintgrid = relationship("SprintGridRec", back_populates="year_sprintgrid")
    sprintqualifcations = relationship("SprintQualifyingRec", back_populates="year_sprintqualifcations")
    sprintresult = relationship("SprintResultRec", back_populates="year_sprintresult")
    startinggrid = relationship("StartingGridRec", back_populates="year_startinggrid")


    __table_args__ = (
        {'schema': 'public'}
    )

    def __repr__(self):
        return f"<YearRec(Year='{self.Year}')>"

class DriverRec(Base):
    __tablename__ ='Drivers'
    DriverNumber = Column(Integer, primary_key=True)
    Name = Column(String(40))
    Nationality = Column(String(30))

    # dr_fastestlaps = relationship("FastestLapsRec", back_populates="driver_fastestlaps")
    # dr_pitstopssummary = relationship("PitStopSummaryRec", back_populates="driver_pitstopssummary")
    # dr_practice1 = relationship("Practice1Rec", back_populates="driver_practice1")
    # dr_practice2 = relationship("Practice2Rec", back_populates="driver_practice2")
    # dr_practice3 = relationship("Practice3Rec", back_populates="driver_practice3")
    # dr_qualifications = relationship("QualifyingRec", back_populates="driver_qualifications")
    # dr_raceresults = relationship("RaceResultRec", back_populates="driver_raceresults")
    # dr_sprintgrid = relationship("SprintGridRec", back_populates="driver_sprintgrid")
    # dr_sprintqualifcations = relationship("SprintQualifyingRec", back_populates="driver_sprintqualifcations")
    # dr_sprintresult = relationship("SprintResultRec", back_populates="driver_sprintresult")
    # dr_startinggrid = relationship("StartingGridRec", back_populates="driver_startinggrid")

    __tableargs__ = (
        {'schema': 'public'}
    )

    def __repr__(self):
        return f"<Driver(number={self.Number}, name='{self.Name}', nationality='{self.Nationality}')>"

class FastestLapsRec(Base):
    __tablename__ = 'FastestsLaps'
    Year = Column(Integer, ForeignKey('public.Years.Year'), primary_key=True)
    Country = Column(String(30), primary_key=True)
    Position = Column(Integer)
    # DriverNumber = Column(Integer, ForeignKey('public.Drivers.Number'))
    DriverNumber = Column(Integer)
    Driver = Column(String(60), primary_key=True)
    Car = Column(String(60))
    Lap = Column(Integer)
    TimeOfDay = Column(String(30))
    Time = Column(String(20))
    AvgSpeed = Column(Float)

    year_fastestlaps = relationship("YearRec", back_populates="fastestlaps")
    # driver_fastestlaps = relationship("DriverRec", back_populates="dr_fastestlaps")

    __table_args__ = (
        UniqueConstraint('Year', 'Country', 'Driver'),
        {'schema': 'public'}
    )

    def __repr__(self):
        return f"<FastestLapsRec(Year={self.Year}, Country='{self.Country}', Position={self.Position}, Driver='{self.Driver}', Car='{self.Car}', Lap='{self.Lap}', Time='{self.Time}', AvgSpeed='{self.AvgSpeed}')>"
    

class PitStopSummaryRec(Base):
    __tablename__ = 'PitStops'
    Year = Column(Integer, ForeignKey('public.Years.Year'), primary_key=True)
    Country = Column(String(30), primary_key=True)
    Stop = Column(Integer, primary_key=True)
    # DriverNumber = Column(Integer, ForeignKey('public.Drivers.Number'))
    DriverNumber = Column(Integer)
    Driver = Column(String(60), primary_key=True)
    Car = Column(String(60))
    Lap = Column(Integer)
    TimeOfDay = Column(String(30))
    Time = Column(String(20))
    Total = Column(String(20))

    year_pitstopssummary = relationship("YearRec", back_populates="pitstopssummary")
    # driver_pitstopssummary = relationship("DriverRec", back_populates="dr_pitstopssummary")

    __table_args__ = (
        UniqueConstraint('Year', 'Country', 'Stop', 'Driver'),
        {'schema': 'public'}
    )

    def __repr__(self):
        return f"<FastestLapsRec(Year={self.Year}, Country='{self.Country}', Stop={self.Stops}, Driver='{self.Driver}', Car='{self.Car}', Lap='{self.Lap}', Time='{self.Time}', Total='{self.Total}')>"
    

class Practice1Rec(Base):
    __tablename__ = 'Practice1'
    Year = Column(Integer, ForeignKey('public.Years.Year'), primary_key=True)
    Country = Column(String(30), primary_key=True)
    Position = Column(Integer)
    # DriverNumber = Column(Integer, ForeignKey('public.Drivers.Number'))
    DriverNumber = Column(Integer)
    Driver = Column(String(60), primary_key=True)
    Car = Column(String(60))
    Time = Column(String(20))
    Gap = Column(String(20))
    Laps = Column(Integer)

    year_practice1 = relationship("YearRec", back_populates="practice1")
    # driver_practice1 = relationship("DriverRec", back_populates="dr_practice1")

    __table_args__ = (
        UniqueConstraint('Year', 'Country', 'Driver'),
        {'schema': 'public'}
    )

    def __repr__(self):
        return f"<Practice1Rec(Year={self.Year}, Country='{self.Country}', Position={self.Position}, Driver='{self.Driver}', Car='{self.Car}', Time='{self.Time}', Gap='{self.Gap}', Laps='{self.Laps}')>"


class Practice2Rec(Base):
    __tablename__ = 'Practice2'
    Year = Column(Integer, ForeignKey('public.Years.Year'), primary_key=True)
    Country = Column(String(30), primary_key=True)
    Position = Column(Integer)
    # DriverNumber = Column(Integer, ForeignKey('public.Drivers.Number'))
    DriverNumber = Column(Integer)
    Driver = Column(String(60), primary_key=True)
    Car = Column(String(60))
    Time = Column(String(20))
    Gap = Column(String(20))
    Laps = Column(Integer)

    year_practice2 = relationship("YearRec", back_populates="practice2")
    # driver_practice2 = relationship("DriverRec", back_populates="dr_practice2")

    __table_args__ = (
        UniqueConstraint('Year', 'Country', 'Driver'),
        {'schema': 'public'}
    )

    def __repr__(self):
        return f"<Practice2Rec(Year={self.Year}, Country='{self.Country}', Position={self.Position}, Driver='{self.Driver}', Car='{self.Car}', Time='{self.Time}', Gap='{self.Gap}', Laps='{self.Laps}')>"
    
class Practice3Rec(Base):
    __tablename__ = 'Practice3'
    Year = Column(Integer, ForeignKey('public.Years.Year'), primary_key=True)
    Country = Column(String(30), primary_key=True)
    Position = Column(Integer)
    # DriverNumber = Column(Integer, ForeignKey('public.Drivers.Number'))
    DriverNumber = Column(Integer)
    Driver = Column(String(60), primary_key=True)
    Car = Column(String(60))
    Time = Column(String(20))
    Gap = Column(String(20))
    Laps = Column(Integer)

    year_practice3 = relationship("YearRec", back_populates="practice3")
    # driver_practice3 = relationship("DriverRec", back_populates="dr_practice3")

    __table_args__ = (
        UniqueConstraint('Year', 'Country', 'Driver'),
        {'schema': 'public'}
    )

    def __repr__(self):
        return f"<Practice3Rec(Year={self.Year}, Country='{self.Country}', Position={self.Position}, Driver='{self.Driver}', Car='{self.Car}', Time='{self.Time}', Gap='{self.Gap}', Laps='{self.Laps}')>"

class QualifyingRec(Base):
    __tablename__ = 'Qualifications'
    Year = Column(Integer, ForeignKey('public.Years.Year'), primary_key=True)
    # Year = Column(Integer, primary_key=True)
    Country = Column(String(30), primary_key=True)
    Position = Column(Integer)
    # DriverNumber = Column(Integer, ForeignKey('public.Drivers.DriverNumber'))
    DriverNumber = Column(Integer)
    Driver = Column(String(60), primary_key=True)
    Car = Column(String(60))
    Q1 = Column(String(20))
    Q2 = Column(String(20))
    Q3 = Column(String(20))
    Laps = Column(Integer)

    #year = relationship("YearRec", backref="qualifications")
    year_qualifications = relationship("YearRec", back_populates="qualifications")
    # driver_qualifications = relationship("DriverRec", back_populates="dr_qualifications")

    __table_args__ = (
        UniqueConstraint('Year', 'Country', 'Driver'),
        {'schema': 'public'}
    )

    def __repr__(self):
        return f"<QualifyingRec(Year={self.Year}, Country='{self.Country}', Position={self.Position}, Driver='{self.Driver}', Car='{self.Car}')>"
    
class RaceResultRec(Base):
    __tablename__='RaceResults'
    Year = Column(Integer, ForeignKey('public.Years.Year'), primary_key=True)
    Country = Column(String(30), primary_key=True)
    Position = Column(Integer)
    # DriverNumber = Column(Integer, ForeignKey('public.Drivers.Number'))
    DriverNumber = Column(Integer)
    Driver = Column(String(60), primary_key=True)
    Car = Column(String(60))
    Laps = Column(Integer)
    Time = Column(String(20)) # String because driver can retire from a race or be overlapped then this field will be DNF / +number_of_laps
    Points = Column(Integer)

    year_raceresults = relationship("YearRec", back_populates="raceresults")
    # driver_raceresults = relationship("DriverRec", back_populates="dr_raceresults")

    __tableargs__= (
        {'schema': 'public'}
    )

    def __repr__(self):
        return f"<RaceResultRec(Year={self.Year}, Country='{self.Country}', Driver='{self.Driver}', Car='{self.Car}', Position={self.Position}, Points='{self.Points}', Time='{self.Time}')>"
    
class SprintGridRec(Base):
    __tablename__ = 'SprintGrid'
    Year = Column(Integer, ForeignKey('public.Years.Year'), primary_key=True)
    Country = Column(String(30), primary_key=True)
    Position = Column(Integer)
    # DriverNumber = Column(Integer, ForeignKey('public.Drivers.Number'))
    DriverNumber = Column(Integer)
    Driver = Column(String(60), primary_key=True)
    Car = Column(String(60))
    Time = Column(String(20))

    year_sprintgrid = relationship("YearRec", back_populates="sprintgrid")
    # driver_sprintgrid = relationship("DriverRec", back_populates="dr_sprintgrid")

    __table_args__ = (
        UniqueConstraint('Year', 'Country', 'Driver'),
        {'schema': 'public'}
    )

    def __repr__(self):
        return f"<SprintGrid(Year={self.Year}, Country='{self.Country}', Position={self.PoPositions}, Driver='{self.Driver}', Car='{self.Car}', Time='{self.Time}')>"
    
class SprintQualifyingRec(Base):
    __tablename__ = 'SprintQualifications'
    Year = Column(Integer, ForeignKey('public.Years.Year'), primary_key=True)
    Country = Column(String(30), primary_key=True)
    Position = Column(Integer)
    # DriverNumber = Column(Integer, ForeignKey('public.Drivers.Number'))
    DriverNumber = Column(Integer)
    Driver = Column(String(60), primary_key=True)
    Car = Column(String(60))
    Q1 = Column(String(20))
    Q2 = Column(String(20))
    Q3 = Column(String(20))
    Laps = Column(Integer)

    year_sprintqualifcations = relationship("YearRec", back_populates="sprintqualifcations")
    # driver_sprintqualifcations = relationship("DriverRec", back_populates="dr_sprintqualifcations")

    __table_args__ = (
        UniqueConstraint('Year', 'Country', 'Driver'),
        {'schema': 'public'}
    )

    def __repr__(self):
        return f"<SprintQualifyingRec(Year={self.Year}, Country='{self.Country}', Position={self.Position}, Driver='{self.Driver}', Car='{self.Car}')>"
    
class SprintResultRec(Base):
    __tablename__='SprintResults'
    Year = Column(Integer, ForeignKey('public.Years.Year'), primary_key=True)
    Country = Column(String(30), primary_key=True)
    Position = Column(Integer)
    # DriverNumber = Column(Integer, ForeignKey('public.Drivers.Number'))
    DriverNumber = Column(Integer)
    Driver = Column(String(60), primary_key=True)
    Car = Column(String(60))
    Laps = Column(Integer)
    Time = Column(String(20)) # String because driver can retire from a sprint or be overlapped then this field will be DNF / +number_of_laps
    Points = Column(Integer)

    year_sprintresult = relationship("YearRec", back_populates="sprintresult")
    # driver_sprintresult = relationship("DriverRec", back_populates="dr_sprintresult")

    __tableargs__= (
        {'schema': 'public'}
    )

    def __repr__(self):
        return f"<SprintResultRec(Year={self.Year}, Country='{self.Country}', Driver='{self.Driver}', Car='{self.Car}', Position={self.Position}, Points='{self.Points}', Time='{self.Time}')>"
    

class StartingGridRec(Base):
    __tablename__ = 'StartingGrid'
    Year = Column(Integer, ForeignKey('public.Years.Year'), primary_key=True)
    Country = Column(String(30), primary_key=True)
    Position = Column(Integer)
    # DriverNumber = Column(Integer, ForeignKey('public.Drivers.Number'))
    DriverNumber = Column(Integer)
    Driver = Column(String(60), primary_key=True)
    Car = Column(String(60))
    Time = Column(String(30))

    year_startinggrid = relationship("YearRec", back_populates="startinggrid")
    # driver_startinggrid = relationship("DriverRec", back_populates="dr_startinggrid")

    __table_args__ = (
        UniqueConstraint('Year', 'Country', 'Driver'),
        {'schema': 'public'}
    )

    def __repr__(self):
        return f"<StartingGridRec(Year={self.Year}, Country='{self.Country}', Position={self.Position}, Driver='{self.Driver}', Car='{self.Car}', Time='{self.Time}')>"


