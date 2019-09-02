AC_PREREQ([2.69])
AC_INIT([RTE+RRTMGP], [1.0.0], [], [],
  [https://github.com/RobertPincus/rte-rrtmgp])
AC_CONFIG_MACRO_DIR([m4])
AC_CONFIG_AUX_DIR([config])
AC_CONFIG_SRCDIR([rte/mo_rte_sw.F90])

AC_ARG_ENABLE([silent-rules],
  [AC_HELP_STRING([--enable-silent-rules],
     [less verbose build output (undo: "make V=1") @<:@default=yes@:>@])],
  [AS_IF([test x"$enableval" != xno], [enable_silent_rules=yes])],
  [enable_silent_rules=yes])

AC_ARG_ENABLE([module-tracking],
  [AC_HELP_STRING([--enable-module-tracking],
     [enable Fortran module tracking rules, which might slow down the
rebuilding but prevent make from failing when a required Fortran module file is
missing (e.g. accidentally deleted after the first build)
@<:@default=no@:>@])],
  [AS_IF([test x"$enableval" != xno], [enable_module_tracking=yes])],
  [enable_module_tracking=no])

AC_ARG_ENABLE([openacc],
  [AC_HELP_STRING([--enable-openacc],
     [enable OpenACC kernels @<:@default=no@:>@])],
  [AS_IF([test x"$enableval" != xno], [enable_openacc=yes])],
  [enable_openacc=no])

AC_PROG_FC
AC_LANG([Fortran])
ACX_FC_PP_SRCEXT([F90])
ACX_COMPILER_FC_VENDOR

ACX_FC_LINE_LENGTH([unlimited])
ACX_FC_MODULE_NAMING(
  [AC_SUBST([FCMODEXT], ["$acx_cv_fc_module_naming_ext"])
   AC_SUBST([FCMODUC], ["$acx_cv_fc_module_naming_upper"])])
ACX_FC_MODULE_IN_FLAG([AC_SUBST([FCMODINC], ["$acx_cv_fc_module_in_flag"])])
ACX_FC_MODULE_OUT_FLAG([AC_SUBST([FCMODOUT], ["$acx_cv_fc_module_out_flag"])])
ACX_LANG_MACRO_FLAG([], [:])
ACX_SHLIB_FC_RPATH_FLAG

AC_SUBST([DEFAULT_VERBOSITY], [0])
AS_VAR_IF([enable_silent_rules], [no], [DEFAULT_VERBOSITY=1])

AS_VAR_IF([enable_module_tracking], [yes],
  [AC_SUBST([MODULE_TRACKING_ENABLED], [''])],
  [AC_SUBST([MODULE_TRACKING_ENABLED], ['#'])])

AS_VAR_IF([enable_openacc], [yes],
  [ACX_LANG_OPENACC_FLAG(
     [AS_VAR_APPEND([FCFLAGS], [" $acx_cv_fc_openacc_flag"])])
   ACX_LANG_MACRO_CHECK_VALUE([_OPENACC], [201711 201510 201308 201306 201111])
   AS_IF(
     [test x"$acx_macro_value" = xunknown],
     [AC_MSG_WARN([unable to detect supported OpenACC version (at least dnl
version 2.6 is required): the compilation of the OpenACC kernels might fail])],
     [test "$acx_macro_value" -lt 201711 >&AS_MESSAGE_LOG_FD 2>&1],
     [AC_MSG_ERROR([Fortran compiler does not support OpenACC 2.6 (201711): dnl
disable OpenACC support (--disable-openacc)])])
   AC_SUBST([OPENACC_ENABLED], [''])
   AC_SUBST([OPENACC_DISABLED], ['#'])],
  [ACX_LANG_MACRO_CHECK_DEFINED([_OPENACC])
   AS_VAR_IF([acx_macro_defined], [yes],
     [AC_MSG_ERROR([Fortran compiler enables OpenACC support by default: dnl
set FCFLAGS accordingly to disable it])])
   AC_SUBST([OPENACC_ENABLED], ['#'])
   AC_SUBST([OPENACC_DISABLED], [''])])

ACX_LANG_PACKAGE_INIT([NetCDF], ["$FCMODINC"], [-L "$acx_cv_fc_rpath_flag"])
ACX_LANG_PACKAGE_INIT([GPTL], ["$FCMODINC"], [-L "$acx_cv_fc_rpath_flag"])
AC_SUBST([DEPGEN_EXTERNAL_MODS], [netcdf,gptl])

dnl Check for NetCDF
acx_have_netcdf=no
acx_save_FCFLAGS=$FCFLAGS
NETCDF_FCFLAGS=${NETCDF_FCFLAGS-$acx_fc_NetCDF_inc_search_args}
FCFLAGS="$NETCDF_FCFLAGS $acx_save_FCFLAGS"
ACX_FC_MODULE_CHECK([netcdf],
  [ACX_LANG_LIB_SEARCH([NETCDF_FCLIBS], [nf90_open],
     [ASX_PREPEND_LDFLAGS([$acx_fc_NetCDF_lib_search_args],
        [-lnetcdff], [-lnetcdff -lnetcdf])],
     [NETCDF_FCLIBS=$acx_cv_fc_lib_func_NF90_OPEN
      acx_have_netcdf=yes], [:],
     [AC_LANG_PROGRAM([],
[[      use netcdf, only: nf90_open, NF90_NOWRITE
      implicit none
      integer :: status, ncid
      status = nf90_open('conftest.nc', NF90_NOWRITE, ncid)]])])], [:])
FCFLAGS=$acx_save_FCFLAGS
AS_VAR_IF([acx_have_netcdf], [no],
  [AC_MSG_WARN([NetCDF is not available: the test suite is disabled])
   NETCDF_FCFLAGS= ; NETCDF_FCLIBS=
   AC_SUBST([TESTS_ENABLED], ['#'])],
  [AC_SUBST([TESTS_ENABLED], [''])])

dnl Check for GPTL
acx_have_gptl=no
acx_save_FCFLAGS=$FCFLAGS
GPTL_FCFLAGS=${GPTL_FCFLAGS-$acx_fc_GPTL_inc_search_args}
FCFLAGS="$GPTL_FCFLAGS $acx_save_FCFLAGS"
ACX_FC_MODULE_CHECK([gptl],
  [ACX_LANG_LIB_SEARCH([GPTL_FCLIBS], [gptlstart],
     [ASX_PREPEND_LDFLAGS([$acx_fc_GPTL_lib_search_args],
        [-lgptlf], [-lgptlf -lgptl])],
     [GPTL_FCLIBS=$acx_cv_fc_lib_func_GPTLSTART
      acx_have_gptl=yes], [:],
     [AC_LANG_PROGRAM([],
[[      use gptl, only: gptlstart
      implicit none
      integer :: status
      status = gptlstart('conftest')]])])], [:])
FCFLAGS=$acx_save_FCFLAGS
AS_IF([test x"$acx_have_gptl" = xyes && dnl
test x"acx_cv_fc_macro_flag" != xunknown],
  [AS_VAR_APPEND([FCFLAGS], [" ${acx_cv_fc_macro_flag}USE_TIMING"])],
  [GPTL_FCFLAGS= ; GPTL_FCLIBS=])


dnl Check for AR and ARFLAGS
AC_ARG_VAR([AR], [archiver command])
AC_ARG_VAR([ARFLAGS], [archiver flags])
ARFLAGS=${ARFLAGS-cr}
ACX_PROG_SEARCH([AR], [ar],
  [AC_COMPILE_IFELSE([AC_LANG_PROGRAM],
     [acx_ar_try="$acx_candidate ${ARFLAGS} libconftest.a dnl
conftest.$ac_objext >&AS_MESSAGE_LOG_FD"
      _AC_DO_VAR([acx_ar_try])
      rm -f libconftest.a])
   test "$ac_status" -eq 0 >/dev/null 2>&1],
  [AR=$acx_candidate])

dnl Check for PYTHON
AC_ARG_VAR([PYTHON], [Python interpreter command])dnl
ACX_PROG_SEARCH([PYTHON], [python3 python],
  [acx_python_try="$acx_candidate $srcdir/mkhelper/depgen.py -h dnl
>&AS_MESSAGE_LOG_FD"
   _AC_DO_VAR([acx_python_try])],
  [PYTHON=$acx_candidate])

AS_VAR_IF([TESTS_ENABLED], [],
  [AC_MSG_CHECKING([whether Python is compatible with the test suite])
   acx_python_try="$acx_candidate -c 'import sys; exit(sys.version_info@<:@0@:>@ < 3)' >&AS_MESSAGE_LOG_FD"
   _AC_DO_VAR([acx_python_try])
   AS_IF([test $? -eq 0],
     [AC_MSG_RESULT([yes])],
     [AC_MSG_RESULT([no])
      AC_MSG_WARN([Python is not compatible with the test suite: the test suite is disabled])
      TESTS_ENABLED='#'])])

AS_VAR_IF([TESTS_ENABLED], [],
  [for acx_python_mod in 'netCDF4' 'xarray' 'dask' 'toolz'; do
     AC_MSG_CHECKING([whether Python module '$acx_python_mod' is available])
     acx_python_try="$PYTHON -c 'import $acx_python_mod' >&AS_MESSAGE_LOG_FD"
     _AC_DO_VAR([acx_python_try])
     AS_IF([test $? -eq 0],
       [AC_MSG_RESULT([yes])],
       [AC_MSG_RESULT([no])
        AC_MSG_WARN([Python module '$acx_python_mod' is not available: the dnl
test suite is disabled])
        TESTS_ENABLED='#'
        break])
   done])

AC_PROG_INSTALL
AC_PROG_MKDIR_P

AC_CONFIG_FILES([
    examples/rfmip-clear-sky/rfmip-clear-sky.test
], [chmod a+x "$ac_file"])

AC_CONFIG_LINKS([
    examples/rfmip-clear-sky/rrtmgp-data-lw-g256-2018-12-04.nc:rrtmgp/data/rrtmgp-data-lw-g256-2018-12-04.nc
    examples/rfmip-clear-sky/rrtmgp-data-sw-g224-2018-12-04.nc:rrtmgp/data/rrtmgp-data-sw-g224-2018-12-04.nc
])

AC_CONFIG_FILES([
    Makefile
    depgen.config
])

dnl An additional step to generate dummy dependencies:
AC_CONFIG_COMMANDS([depfiles],
  [${MAKE-make} dummy-depend >/dev/null 2>&AS_MESSAGE_LOG_FD
   sleep 1
   touch Makefile])

AC_OUTPUT
