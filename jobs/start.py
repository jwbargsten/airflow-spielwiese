#!/usr/bin/env python

import importlib
import logging
import sys
import os

logger = logging.getLogger(__name__)


def main():
    # the first argument is <modulename>:<functionname>
    (prog, jobname, *rest) = sys.argv
    sys.argv = [prog, *rest]
    (mod_name, fn_name) = jobname.split(":", maxsplit=1)
    logger.info(f"Starting job {jobname}")
    mod = importlib.import_module(mod_name)
    fn = getattr(mod, fn_name)
    fn()


def _get_log_level():
    loglevel = os.environ.get("LOG_LEVEL", "INFO")
    numeric_level = getattr(logging, loglevel.upper(), None)

    if not isinstance(numeric_level, int):
        raise ValueError("Invalid log level: %s" % loglevel)

    return numeric_level


def _init_logging_system():
    log_dtfmt = "%Y-%m-%d %H:%M:%S"
    log_fmt = "%(asctime)s %(levelname)-5s %(name)s.%(funcName)s: %(message)s"
    log_level = _get_log_level()
    logging.basicConfig(level=log_level, format=log_fmt, datefmt=log_dtfmt)
    logger.debug("logging system initiated")


if __name__ == "__main__":
    _init_logging_system()
    main()
