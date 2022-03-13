# sqlalchemy-challenge
This assignment consisted of using Python and SQLAlchemy to do basic climate analysis and create an API.

# What the code does (in general terms)
The code uses SQLAlchemy ORM queries, Pandas, and Matplotlib to analyze temperature and precipitation data in Hawaii over various time periods.

# What the code calculates

The **climate_starter.ipynb** code uses queries and data frames to do the following:
    
    1. Create a data frame with the date and precipitation amount for each date in the last year of data.

    2. Create a bar plot of the last year of precipitation data.

    3. Display the summary statistic for the last year of precipitation data.

    4. Finds the lowest, highest, and average temperature of the most active weather station.

    5. Create a data frame with the date and temperature for each date in the last year of data.

    6. Creates a histogram of the last year of temperature data.

The **app.py** code contains queries that will display the following in an API:

    1. All routes that are available.
    
    2. A JSON list of precipitation data for the previous year.

    3. A JSON list of stations from the dataset.

    4. A JSON list of temperature observations (TOBS) for the previous year.

    5. A JSON list of the minimum temperature, the average temperature, and the max temperature from given start date to the end of the data.

    6. A JSON list of the minimum temperature, the average temperature, and the max temperature for a given start-end range.

The **temp_analysis_bonus_1_starter.ipynb** reads the "hawaii_measurements.csv" and finds the following:

    1. The average temperature in June at all stations for all years in the data set.

    2. The average temperature in December at all stations for all years in the data set.

    3. The p-value from an un-paired t-test to determine if the difference in means between June and December is statistically significant.

The **temp_analysis_bonus_2_starter.ipynb** code uses queries and data frames to do the following for a specified date range:

    1. Plot the min, avg, and max temperature for in bar chart, with the peak-to-peak (TMAX-TMIN) value as the y error bar (YERR).

    2. Create a list of rainfall per weather station.

    3. 
