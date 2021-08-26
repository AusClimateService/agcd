## AGCD data processing for CAFE analysis

Validation of the Climate Analysis Forecast Ensemble dataset
([CAFE](https://research.csiro.au/dfp/cafe-csiro-decadal-prediction-system/))
often involves comparison against
Australian Gridded Climate Data dataset
([AGCD](http://www.bom.gov.au/metadata/catalogue/19115/ANZCW0503900567)).

This repository contains the code used to:
- Convert the netCDF AGCD data files to zarr format (`nc_to_zarr.py`)
- Regrid AGCD data to CAFE grid (`regrid_agcd_to_cafe.py`)

Those python scripts were executed to produce the data in `../data`
by running the folowing at the command line:
- `make zarr TIMESCALE=monthly` (convert monthly AGCD data to zarr format)
- `make regrid TIMESCALE=monthly` (regrid monthly AGCD data to CAFE grid)
- `make zarr TIMESCALE=monthly` (convert daily AGCD data to zarr format)
- `make regrid TIMESCALE=monthly` (regrid daily data to CAFE grid)

To find out exactly what commands were executed,
run any of those make commands with the `-n` (dry run) and `-B` (force make)
options (e.g. `make -n -B make zarr TIMESCALE=monthly`)
or open any of the files in `../data` and look at the global history attribute.

If you'd like to recreate the software environment that was used to run the python scripts,
run the following at the command line:
```
conda env create -f environment.yml 
```


