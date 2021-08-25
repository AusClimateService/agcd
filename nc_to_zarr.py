"""Convert netCDF files to Zarr collection."""

import argparse
import xarray as xr
import zarr_utils


def main(args):
    """Run the command line program."""

    ds = xr.open_mfdataset(args.infiles,
                           concat_dim='time',
                           combine='nested',
                           data_vars='minimal',
                           coords='minimal',
                           compat='override')
    ds.attrs['history'] = zarr_utils.get_new_log()
    zarr_utils.to_zarr(ds, args.outfile)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)        
    parser.add_argument("infiles", type=str, nargs='*', help="Input netCDF files")
    parser.add_argument("outfile", type=str, help="Output file name (must end in .zarr.zip)")
    args = parser.parse_args()
    main(args)
    