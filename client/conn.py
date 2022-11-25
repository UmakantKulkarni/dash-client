#!/usr/bin/env python3
from ctypes import *
import os.path

current_dir_path = os.path.dirname(os.path.realpath(__file__))
lib = cdll.LoadLibrary(current_dir_path + "/proxy_module.so")


class GoSlice(Structure):
    _fields_ = [("data", POINTER(c_void_p)), ("len", c_longlong),
                ("cap", c_longlong)]


class GoString(Structure):
    _fields_ = [("p", c_char_p), ("n", c_longlong)]


lib.ClientSetup.argtypes = [c_bool, c_bool, c_bool, GoString, GoString]
lib.DownloadSegment.argtypes = [GoString]
lib.CloseConnection.argtypes = []
lib.StartLogging.argtypes = [c_uint]
lib.StopLogging.argtypes = []
lib.FECSetup.argtypes = [c_bool, GoString, c_uint]

import time

last_time = None

schedulerNameEncoded = None


def setupPM(useQUIC,
            useMP,
            keepAlive,
            schedulerName,
            congestionControl='cubic'):
    global schedulerNameEncoded
    schedulerNameEncoded = schedulerName.encode('ascii')
    scheduler = GoString(schedulerNameEncoded, len(schedulerNameEncoded))
    lib.ClientSetup(useQUIC, useMP, keepAlive, scheduler, GoString(b"", 0))


def setupFEC(useFEC, scheme, nDataSymbols):
    schemeEncoded = scheme.encode('ascii')
    schemeGoStr = GoString(schemeEncoded, len(schemeEncoded))
    lib.FECSetup(useFEC, schemeGoStr, nDataSymbols)


def closeConnection():
    lib.CloseConnection()


def download_segment_PM(segment_url):
    segment = GoString(segment_url.encode('ascii'), len(segment_url))
    return lib.DownloadSegment(segment)


def startLogging(period):
    lib.StartLogging(period)


def stopLogging():
    lib.StopLogging()
