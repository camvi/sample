find_package(PkgConfig)

#
# hack to get lack of pkg-config search paths in Cmake
# https://stackoverflow.com/questions/20447821/add-temporarily-path-to-pkg-config-within-cmake-script#26012078
#
set( ENV{PKG_CONFIG_PATH} "$ENV{PKG_CONFIG_PATH}:${CAMVI_SYSDEP_DIR}/lib/pkgconfig" )

pkg_check_modules(PC_LIBZMQ QUIET libzmq)

set(PC_LIBZMQ_LIBRARY_DIRS "${CAMVI_SYSDEP_DIR}/lib")
set(PC_LIBZMQ_INCLUDE_DIRS "${CAMVI_SYSDEP_DIR}/include")

set(ZeroMQ_VERSION ${PC_LIBZMQ_VERSION})
find_library(ZeroMQ_LIBRARY NAMES libzmq.so libzmq.dylib libzmq.dll
             PATHS ${PC_LIBZMQ_LIBDIR} ${PC_LIBZMQ_LIBRARY_DIRS})
find_library(ZeroMQ_STATIC_LIBRARY NAMES libzmq.a libzmq.dll.a libzmq-static.a
             PATHS ${PC_LIBZMQ_LIBDIR} ${PC_LIBZMQ_LIBRARY_DIRS})

add_library(libzmq SHARED IMPORTED)
set_property(TARGET libzmq PROPERTY INTERFACE_INCLUDE_DIRECTORIES ${PC_LIBZMQ_INCLUDE_DIRS})
set_property(TARGET libzmq PROPERTY IMPORTED_LOCATION ${ZeroMQ_LIBRARY})

add_library(libzmq-static STATIC IMPORTED ${PC_LIBZMQ_INCLUDE_DIRS})
set_property(TARGET libzmq-static PROPERTY INTERFACE_INCLUDE_DIRECTORIES ${PC_LIBZMQ_INCLUDE_DIRS})
set_property(TARGET libzmq-static PROPERTY IMPORTED_LOCATION ${ZeroMQ_STATIC_LIBRARY})

if(ZeroMQ_LIBRARY AND ZeroMQ_STATIC_LIBRARY)
    set(ZeroMQ_FOUND ON)
endif()
