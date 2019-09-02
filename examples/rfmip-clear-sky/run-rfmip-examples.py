#! /usr/bin/env python
#
# This script runs runs RRTMGP on the RFMIP off-line test cases
#
import os, subprocess, glob

#
# Run the RFMIP example programs that computes fluxes from netCDF Garand atmosphere files
#
conds_file      = "multiple_input4MIPs_radiation_RFMIP_UColorado-RFMIP-1-2_none.nc"

rfmip_lw_exe_name = "rrtmgp_rfmip_lw"
rfmip_sw_exe_name = "rrtmgp_rfmip_sw"
print("Running RFMIP drivers")
# arguments are block size, input conditions, coefficient files, forcing index, physics index
subprocess.run([os.path.join(os.getcwd(), rfmip_lw_exe_name), "8", conds_file, "rrtmgp-data-lw-g256-2018-12-04.nc"])
subprocess.run([os.path.join(os.getcwd(), rfmip_sw_exe_name), "8", conds_file, "rrtmgp-data-sw-g224-2018-12-04.nc"])
