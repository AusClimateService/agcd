## AGCD data processing for CAFE analysis

Validation of the Climate Analysis Forecast Ensemble dataset
([CAFE](https://research.csiro.au/dfp/cafe-csiro-decadal-prediction-system/))
often involves comparison against
Australian Gridded Climate Data dataset
([AGCD](http://www.bom.gov.au/metadata/catalogue/19115/ANZCW0503900567)).

This repository contains the code used to:
- Convert the netCDF AGCD data files to zarr format (`nc_to_zarr.py`)
- Regrid AGCD data to CAFE grid (`regrid_agcd_to_cafe.py`)

Those python scripts were executed to produce each data file in `../data`
by running the following at the command line:

`agcd_v2_precip_total_r005_monthly_1900-2020.zarr.zip`
- `make zarr TIMESCALE=monthly`
- Converts the version 2 monthly AGCD data (0.05 degree grid) to zarr format

`agcd_v2_precip_total_cafe-grid_monthly_1900-2020.zarr.zip`
- `make regrid TIMESCALE=monthly` 
- Regrids the monthly AGCD data (0.05 degree grid) to the CAFE grid

`agcd_v1_precip_total_r005_daily_1900-2020.zarr.zip`
- `make zarr TIMESCALE=daily`
- Converts the version 2 daily AGCD data (0.05 degree grid) to zarr format

`agcd_v1_precip_total_cafe-grid_daily_1900-2020.zarr.zip`
- `make regrid TIMESCALE=daily` 
- Regrids the daily AGCD data (0.05 degree grid) to the CAFE grid

To find out exactly what commands were executed,
run any of those make commands with the `-n` (dry run) and `-B` (force make)
options (e.g. `make -n -B make zarr TIMESCALE=monthly`)
or open any of the files in `../data` and look at the global history attribute.

If you'd like to recreate the software environment that was used to run the python scripts,
run the following at the command line:
```
conda env create -f environment.yml 
```
Questions or comments on the code are welcome at:  
https://github.com/AusClimateService/agcd/issues



