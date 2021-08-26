.PHONY: zarr regrid clean help

ifeq (${TIMESCALE}, monthly)
  VERSION=v2
  TUNIT=month
else ifeq (${TIMESCALE}, daily)
  VERSION=v1
  TUNIT=day
else ifneq (${MAKECMDGOALS}, help)
  $(error Must specify TIMESCALE=daily or TIMESCALE=monthly at command line) 
endif

AGCD_DIR=/g/data/xv83/dbi599/agcd
PYTHON=/g/data/e14/dbi599/miniconda3/envs/agcd/bin/python
FINAL_YEAR=2020

TARGET_GRID=/g/data/xv83/dcfp/CAFE-f6/c5-d60-pX-f6-19811101/atmos_isobaric_daily.zarr.zip

AGCD_NC := $(sort $(wildcard /g/data/zv2/agcd/${VERSION}/precip/total/r005/01${TUNIT}/agcd_${VERSION}_precip_total_r005_${TIMESCALE}_*.nc))
AGCD_ZARR=${AGCD_DIR}/data/agcd_${VERSION}_precip_total_r005_${TIMESCALE}_1900-${FINAL_YEAR}.zarr.zip
AGCD_REGRIDDED=${AGCD_DIR}/data/agcd_${VERSION}_precip_total_cafe-grid_${TIMESCALE}_1900-${FINAL_YEAR}.zarr.zip

## zarr : convert AGCD data to zarr format
zarr : ${AGCD_ZARR}
${AGCD_ZARR} : 
	${PYTHON} ${AGCD_DIR}/code/nc_to_zarr.py ${AGCD_NC} $@

## regrid : regrid AGCD data to CAFE grid
regrid : ${AGCD_REGRIDDED}
${AGCD_REGRIDDED} : ${AGCD_ZARR} ${TARGET_GRID}
	${PYTHON} ${AGCD_DIR}/code/regrid_agcd_to_cafe.py $< $(word 2,$^) $@

## clean : remove all generated files
clean :
	rm ${AGCD_ZARR} ${AGCD_REGRIDDED}

## help : show this message
help :
	@echo 'make [target] TIMESCALE=[timescale]'
	@echo ''
	@echo 'valid targets:'
	@grep -h -E '^##' ${MAKEFILE_LIST} | sed -e 's/## //g' | column -t -s ':'
	@echo 'valid timescales:'
	@echo 'daily'
	@echo 'monthly'




