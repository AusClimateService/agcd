## AGCD data processing

We take the AGCD data and process...

Step 1: netCDF to Zarr

```
$ python nc_to_zarr.py /g/data/zv2/agcd/v2/precip/total/r005/01month/agcd_v2_precip_total_r005_monthly_*.nc agcd_v2_precip_total_r005_monthly_1900-2020.zarr.zip
```

Step 2: Regrid to CAFE grid

```
$ python regrid_agcd.py agcd_v2_precip_total_r005_monthly_1900-2020.zarr.zip /g/data/xv83/dcfp/CAFE-f6/c5-d60-pX-f6-19811101/atmos_isobaric_daily.zarr.zip agcd_v2_precip_total_cafe-grid_monthly_1900-2020.zarr.zip
```

