
## What is this?

CEPIK-dwnldr is a **extremely simple** program for downloading data of road vehicles registered in Poland. It was created **for educational purposes** as part of the Niebezpiecznik.pl's OSINT course.


It may be usefull during OSINT investigations. Data is downloaded from Polish Central Vehicles and Drivers Record (CEPIK) through API and converted to data frame. User has a few options for writing data to disk (i'm working on better options).

## Technical matters

Script is written in Python 3 and you need some Python modules to use it:
1. requests
2. json
3. pandas
4. re

## How to use it?

Just run it and input required data:

1. Starting date (RRRRMMDD)
2. Ending date (RRRRMMDD)
3. Voivodship code
4. Kind of data you would like to see
- option 1: Vehicles first registered beetwen two dates
- option 2: Vehicles last time registered beetwen two dates
5. Choose the exporting options and a filename.
