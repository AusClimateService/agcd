.PHONY: to-zarr regrid clean help

AGCD_DIR=/g/data/xv83/dbi599/agcd
PYTHON=/g/data/e14/dbi599/miniconda3/envs/agcd/bin/python
TIMESCALE=monthly
FINAL_YEAR=2020

ifeq (${TIMESCALE}, monthly)
  VERSION=v2
  TUNIT=month
else
  VERSION=v1
  TUNIT=day
endif

TARGET_GRID=/g/data/xv83/dcfp/CAFE-f6/c5-d60-pX-f6-19811101/atmos_isobaric_daily.zarr.zip

AGCD_NC := $(sort $(wildcard /g/data/zv2/agcd/${VERSION}/precip/total/r005/01${TUNIT}/agcd_${VERSION}_precip_total_r005_${TIMESCALE}_*.nc))
AGCD_ZARR=${AGCD_DIR}/agcd_${VERSION}_precip_total_r005_${TIMESCALE}_1900-${FINAL_YEAR}.zarr.zip
AGCD_REGRIDDED=${AGCD_DIR}/agcd_${VERSION}_precip_total_cafe-grid_${TIMESCALE}_1900-${FINAL_YEAR}.zarr.zip

## to-zarr : convert AGCD data to zarr format
to-zarr : ${AGCD_ZARR}
${AGCD_ZARR} : 
	${PYTHON} ${AGCD_DIR}/nc_to_zarr.py ${AGCD_NC} $@

## regrid : regrid AGCD data to CAFE grid
regrid : ${AGCD_REGRIDDED}
${AGCD_REGRIDDED} : ${AGCD_ZARR} ${TARGET_GRID}
	${PYTHON} ${AGCD_DIR}/regrid_agcd.py $< $(word 2,$^) $@

## clean : remove all generated files
clean :
	rm ${AGCD_ZARR} ${AGCD_REGRIDDED}

## help : show this message
help :
	@echo 'make [target]'
	@echo ''
	@echo 'valid targets:'
	@grep -h -E '^##' ${MAKEFILE_LIST} | sed -e 's/## //g' | column -t -s ':'

