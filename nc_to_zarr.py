"""Convert netCDF files to Zarr collection."""

import argparse
import xarray as xr
import zarr_utils


def main(args):
    """Run the command line program."""

    if args.dask_client:
        zarr_utils.dask_client()

    ds = xr.open_mfdataset(args.infiles,
                           concat_dim='time',
                           combine='nested',
                           data_vars='minimal',
                           coords='minimal',
                           compat='override')
    ds.attrs['history'] = zarr_utils.get_new_log()
    ds = ds.chunk({'time': args.chunk_size})
    zarr_utils.to_zarr(ds, args.outfile)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)        
    parser.add_argument("infiles", type=str, nargs='*', help="Input netCDF files")
    parser.add_argument("outfile", type=str, help="Output file name (must end in .zarr.zip)")
    parser.add_argument("--chunk_size", type=int, default=50,
                        help="Size of time axis chunks for writing output file")
    parser.add_argument("--dask_client", action="store_true", default=False,
                        help="Launch dask client on local cluster [default=False]")
    args = parser.parse_args()
    main(args)
    
