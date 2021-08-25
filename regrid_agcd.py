"""Regrid AGCD data to a different rectilinear grid."""
import pdb
import argparse

import numpy as np
import xarray as xr
import xesmf as xe

import zarr_utils


def stack_bounds(bounds1d):
    """Convert 1D bounds to 2D."""

    bounds2d = np.column_stack((bounds1d[0:-1], bounds1d[1:]))
    
    return bounds2d


def flatten_bounds(bounds2d):
    """Convert 2D bounds into 1D.
    
    Args:
      bounds2d (numpy ndarray)
    """
    
    assert bounds2d.ndim == 2
    assert bounds2d.shape[1] == 2
    bounds1d = np.append(bounds2d[:, 0], bounds2d[-1, 1])
    
    return bounds1d
    
    
def get_original_grid(ds):
    """Get details of original grid."""
    
    original_grid = {'lon': ds['lon'].values,
                     'lat': ds['lat'].values,
                     'lon_b': flatten_bounds(ds['lon_bnds'].values),
                     'lat_b': flatten_bounds(ds['lat_bnds'].values)}
    
    return original_grid

    
def get_target_grid(target_ds, original_grid):
    """Get details of target grid."""

    lon = target_ds['lon'].values
    lat = target_ds['lat'].values
    lonb = target_ds['lonb'].values
    latb = target_ds['latb'].values
    
    min_lat = original_grid['lat_b'].min()
    max_lat = original_grid['lat_b'].max()
    min_lon = original_grid['lon_b'].min()
    max_lon = original_grid['lon_b'].max()
    
    min_latb_index = np.searchsorted(latb, min_lat)
    max_latb_index = np.searchsorted(latb, max_lat)
    min_lonb_index = np.searchsorted(lonb, min_lon)
    max_lonb_index = np.searchsorted(lonb, max_lon)

    target_grid = {'lon': lon[min_lonb_index : max_lonb_index - 1],
                   'lat': lat[min_latb_index : max_latb_index - 1],
                   'lon_b': lonb[min_lonb_index : max_lonb_index],
                   'lat_b': latb[min_latb_index : max_latb_index]}
    
    return target_grid


def regrid_data(original_ds, original_grid, target_grid):
    """Regrid data"""
    
    regridder = xe.Regridder(original_grid, target_grid, 'conservative')
    new_ds = regridder(original_ds[['precip']])
    
    lat_bnds = stack_bounds(target_grid['lat_b'])
    lon_bnds = stack_bounds(target_grid['lon_b'])
    new_ds = new_ds.assign_coords({'lat_bnds': (('lat', 'nv'), lat_bnds),
                                   'lon_bnds': (('lon', 'nv'), lon_bnds),
                                   'time_bnds': original_ds['time_bnds']})

    atts_for_removal = ['geospatial_lat_min', 'geospatial_lat_max',
                        'geospatial_lon_min', 'geospatial_lon_max']
    attrs = original_ds.attrs
    for att in atts_for_removal:
        del attrs[att]
    new_ds.attrs = attrs
    
    return new_ds

    
def main(args):
    """Run the command line program."""

    original_ds = xr.open_zarr(args.input_file)  
    original_grid = get_original_grid(original_ds)

    target_ds = xr.open_zarr(args.target_file)
    target_grid = get_target_grid(target_ds, original_grid)

    new_ds = regrid_data(original_ds, original_grid, target_grid)

    old_command_log = {args.input_file: original_ds.attrs['history']}
    new_command_log = zarr_utils.get_new_log(infile_logs=old_command_log)
    new_ds.attrs['history'] = new_command_log
    
    zarr_utils.to_zarr(new_ds, args.output_file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)        
    parser.add_argument("input_file", type=str, help="Zarr file to be regridded")
    parser.add_argument("target_file", type=str, help="Zarr file with target grid")
    parser.add_argument("output_file", type=str, help="Zarr file for output (must end in .zarr.zip)")
    args = parser.parse_args()
    main(args)
    