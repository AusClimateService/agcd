"""Functions for writing Zarr collections"""

import sys
import os
import shutil
import zipfile

import git
import cmdline_provenance as cmdprov


def get_new_log(infile_logs=None):
    """Generate command log for output file.

    Args:
      infile_logs (dict) : keys are file names,
        values are the command log
    """

    repo_dir = sys.path[0]
    try:
        repo = git.Repo(repo_dir)
        repo_url = repo.remotes[0].url.split('.git')[0]
    except git.exc.InvalidGitRepositoryError:
        repo_url = None
    new_log = cmdprov.new_log(code_url=repo_url,
                              infile_logs=infile_logs)

    return new_log


def zip_zarr(zarr_filename, zip_filename):
    """Zip a zarr collection"""
    
    with zipfile.ZipFile(zip_filename, "w", compression=zipfile.ZIP_STORED, allowZip64=True) as fh:
        for root, _, filenames in os.walk(zarr_filename):
            for each_filename in filenames:
                each_filename = os.path.join(root, each_filename)
                fh.write(each_filename, os.path.relpath(each_filename, zarr_filename))


def to_zarr(ds, filename):
    """Write to zarr file.
    
    Args:
      ds (xarray Dataset)
      filename (str)
    
    """
                
    for var in ds.variables:
        ds[var].encoding = {}

    if filename[-8:] == 'zarr.zip':
        zarr_filename = filename[:-4]
    elif filename[-5:] == '.zarr':
        zarr_filename = filename
    else:
        raise ValueError('File name must end in .zarr or .zarr.zip')

    ds.to_zarr(zarr_filename, mode='w', consolidated=True)
    if filename[-4:] == '.zip':
        zip_zarr(zarr_filename, filename)
        shutil.rmtree(zarr_filename)
        