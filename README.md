[![DOI](https://zenodo.org/badge/399305245.svg)](https://zenodo.org/badge/latestdoi/399305245)

## AGCD data processing for CAFE analysis

Validation of the Climate Analysis Forecast Ensemble dataset
([CAFE](https://research.csiro.au/dfp/cafe-csiro-decadal-prediction-system/))
often involves comparison against the
Australian Gridded Climate Data dataset
([AGCD](http://www.bom.gov.au/metadata/catalogue/19115/ANZCW0503900567)).

This repository contains details of the code, data processing steps,
and software environment used to process the original AGCD dataset
(maintained by the Bureau of Meteorology and hosted at `/g/data/zv2/agcd/`)
into a format consistent with the CAFE dataset
(maintained by CSIRO and hosted at `/g/data/xv83/dcfp/`).
This essentially involves converting the original AGCD netCDF files
to Zarr format and then regridding to the CAFE spatial grid.
The processed files are stored at:  
`/g/data/ia39/AGCD/post-processed/data/`

### Code

The following Python scripts contain the code used to process the AGCD data:
- `nc_to_zarr.py`: converts the netCDF AGCD data files to zarr format 
- `regrid_agcd_to_cafe.py`: regrids AGCD data to the CAFE grid

### Data processing steps

The `Makefile` contains the instructions to build and run the sequence of commands
that were used to execute the Python scripts and produce each data file:

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
or open any of the data files and look at the global history attribute.

### Software environment

The following Python libraries are dependencies for running the code:
`xarray`, `netCDF4`, `dask`, `xesmf`, `gitpython` and `cmdline_provenance`.

When the `Makefile` executes a Python command it uses the conda environment
at `/g/data/e14/dbi599/miniconda3/envs/agcd`,
which has all the dependencies (and their dependencies) installed.
The complete list of packages installed in that environment is shown in `environment.yml`.

If you'd like to recreate that exact software environment
(you don't need to in order to run the `Makefile`),
run the following at the command line:  
```
$ conda env create -f environment.yml
```

### Questions

Questions or comments are welcome at the GitHub repostory
associated with the code:  
https://github.com/AusClimateService/agcd/issues
