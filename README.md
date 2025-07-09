# Contra Costa County Homelessness Services Analysis

## Data Collection

I used California government data and fetched the records using their API with paginated calls. Each dataframe was filtered by location ID `CA-505`, which corresponds to the Contra Costa County Continuum of Care. I decided to keep each dataframe as a separate table.

## Exploratory Data Analysis

I created simple SQL queries to retrieve data and sort it by calendar year and person demographic, including disabled status, veteran status, age group, and race/ethnicity.

The time series graphs can be found here: https://sanjanarattan-ccch3-eda-exxevd.streamlit.app/

## Findings from Initial Analysis

Overall, the number of persons receiving homelessness services has been increasing after a dip in 2020, which may be due to service interruptions during the COVID-19 pandemic. The data analysis does not yet support whether the increase is due to more people becoming homeless or if services are reaching more individuals.
