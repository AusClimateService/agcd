"""Functions for file I/O"""

import pdb
import os
import shutil
import zipfile
import xarray as xr


def zip_zarr(zarr_filename, zip_filename):
    """Zip a zarr collection"""
    
    with zipfile.ZipFile(zip_filename, "w", compression=zipfile.ZIP_STORED, allowZip64=True) as fh:
        for root, _, filenames in os.walk(zarr_filename):
            for each_filename in filenames:
                each_filename = os.path.join(root, each_filename)
                fh.write(each_filename, os.path.relpath(each_filename, zarr_filename))


def to_zarr(ds, filename):
    """Write to zarr file"""
                
    for var in ds.variables:
        ds[var].encoding = {}

    if filename[-4:] == '.zip':
        zarr_filename = filename[:-4]
    else:
        zarr_filename = filename

    ds.to_zarr(zarr_filename, mode='w', consolidated=True)
    if filename[-4:] == '.zip':
        zip_zarr(zarr_filename, filename)
        shutil.rmtree(zarr_filename)