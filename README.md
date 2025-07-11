# WOVOdat
Unofficial python package for World Organization of Volcano Observatories (WOVO) database (WOVOdat). 

WOVOdat is a comprehensive global database on volcanic unrest aimed at understanding pre-eruptive processes and improving eruption forecasts. WOVOdat is brought to you by WOVO (World Organization of Volcano Observatories) and presently hosted at the Earth Observatory of Singapore.

A lack of standardization in data formats and database architectures has made it nearly impossible to do comparative studies of volcanic unrest, or to search data for analogues to any current unrest. WOVOdat fills this gap by translating and compiling this myriad of data into common formats with the goal to make them freely web-accessible, for reference during volcanic crises, comparative studies, and basic research on pre-eruptive processes.

Using WOVOdat, scientists wishing to study how volcanoes prepare to erupt will be able to find a wealth of historical data at their fingertips. Scientists needing to forecast the outcome of a fresh volcanic crisis will be able to search for analogues, find the past outcomes, and estimate (changing) probabilities of how the fresh unrest will evolve. 

WOVOdat Homepage: https://wovodat.org/

# 1. How to install
Make sure you have python `>=3.10`. You can install the package using `pip`:
```python
pip install wovodat
```

# 2. How to use
You can check `examples` directory how to use the WOVOdat package using jupyter notebook.
In short you can use it like this:

```python
from wovodat import WOVOdat

wovo = WOVOdat()

wovo.download(
    smithsonian_id="273083",
    data_type_code="6.5",
    start_date="1991-05-10",
    end_date="1991-05-17",
    username="martanto",
    email="martanto@live.com",
    affiliation="CVGHM",
    extract_zip=True,
)
```     
More detailed information can be seen in the next step.

## 2.1 Import the module
Import the WOVOdat module:
```python
from wovodat import WOVOdat
```

## 2.2 Initiate the module
There are two different ways to import the module:
```python
wovo = WOVOdat(
    # Optional. 
    # Will show detailed information.
    # Default to False.
    verbose=True, 
    
    # Optional. 
    # For debugging purposes. Eg: For development.
    # Default to False.
    debug=True, # Optional. Default to False. Can be removed
)
```
or, just omit the parameters:
```python
wovo = WOVOdat()
```

## 2.3 (Optional) List of supported data types
Call this attribute to get list of the supported data types. The column `code` can be used as reference to `data_type_code` parameter in step **2.5**
```python
#%%
wovo.data_types
```
Example output:

| No |Categories            | Data Type                         | Code |
|----|----------------------|-----------------------------------|------|
| 0  |Deformation Data      | Angle                             | 1.1  |
| 1  |Deformation Data      | EDM                               | 1.2  |
| 2  |Deformation Data      | GPS                               | 1.3  |
| 3  |Deformation Data      | GPS Vector                        | 1.4  |
| 4  |Deformation Data      | Levelling                         | 1.5  |
| 5  |Deformation Data      | Insar                             | 1.6  |
| 6  |Deformation Data      | Strain                            | 1.7  |
| 7  |Deformation Data      | Electronic Tilt                   | 1.8  |
| 8  |Deformation Data      | Tilt Vector                       | 1.9  |
| 9  |Fields Data           | Magnetic Fields                   | 2.1  |
| 10 |Fields Data           | Gravity Fields                    | 2.2  |
| 11 |Fields Data           | Electric Fields                   | 2.3  |
| 12 |Fields Data           | Magnetic Vector                   | 2.4  |
| 13 |Gas Data              | Sample Gas                        | 3.1  |
| 14 |Gas Data              | Soil Efflux                       | 3.2  |
| 15 |Gas Data              | Plume from Ground based station   | 3.3  |
| 16 |Gas Data              | Plume From Satellite/Airplane     | 3.4  |
| 17 |Hydrologic Sample Data| Hydrology                         | 4.1  |
| 18 |Meteo Data            | Meteo                             | 5.1  |
| 19 |Seismic Data          | Seismic Event From Network        | 6.1  |
| 20 |Seismic Data          | Seismic Event From Single Station | 6.2  |
| 21 |Seismic Data          | Seismic Tremor                    | 6.3  |
| 22 |Seismic Data          | Seismic Intensity                 | 6.4  |
| 23 |Seismic Data          | Seismic Interval                  | 6.5  |
| 24 |Seismic Data          | RSAM                              | 6.6  |
| 25 |Seismic Data          | SSAM                              | 6.7  |
| 26 |Thermal Data          | Thermal from Ground based station | 7.1  |
| 27 |Thermal Data          | Thermal From Satellite/Airplane   | 7.2  |

## 2.4 (Optional) Get data availability
This attribute will download the data availability from WOVOdat page.
```python
wovo.availability
```
Example of the results:

|No|vd_name        |data_type           |stime              |etime              |rows_of_data|
|------|---------------|--------------------|-------------------|-------------------|------------|
|0     |Abu            |seismic event       |1920-06-14 07:39:16|2019-02-28 23:42:51|5223        |
|1     |Acamarachi     |seismic event       |1959-09-19 13:37:30|2020-09-19 03:21:29|104         |
|2     |Acatenango     |seismic event       |1951-07-25 18:42:23|2020-11-06 23:29:29|903         |
|3     |Acigöl-Nevsehir|seismic event       |2003-09-19 12:27:32|2020-10-31 09:18:51|162         |
|4     |Adams          |seismic event       |1971-08-21 01:37:38|2017-11-18 09:52:46|438         |
|5     |Adams Seamount |seismic event       |2001-11-22 11:03:47|2001-11-22 11:03:47|1           |
|6     |Adatara        |GPS                 |2002-01-01 00:00:00|2014-01-31 00:00:00|9623        |
|7     |Adatara        |tilt                |2011-10-08 00:00:00|2014-01-31 00:00:00|648         |
|8     |Adatara        |single station event|2002-01-20 09:13:00|2014-01-03 03:32:21|649         |
|9     |Adatara        |seismic interval    |2002-01-20 00:00:00|2014-01-03 00:00:00|250         |

## 2.5 Download Data
Download the data using this method:
```python
wovo.download(
    # VD Number/Smithsonian ID
    smithsonian_id="273083",
    
    # Data type code. You can check step 2.3 
    # In this example, "6.5" is RSAM data type code
    data_type_code="6.5",
    
    # Start and end date. Make sure start date < end date
    # The date format is: YYYY-MM-DD
    start_date="1991-05-10",
    end_date="1991-05-17",
    
    # Mandatory
    # Put your information. 
    username="martanto",
    email="martanto@live.com",
    affiliation="CVGHM",
    
    # Extract downloaded zip file.
    # Default to True.
    extract_zip=True,
)
```