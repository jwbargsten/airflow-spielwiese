#!/usr/bin/env python
# :snippet start-script

import importlib
import logging
import sys
import os

logger = logging.getLogger(__name__)


def main():
    (prog, jobname, *rest) = sys.argv                       # (1)
    sys.argv = [prog, *rest]                                # (2)
    (mod_name, fn_name) = jobname.split(":", maxsplit=1)    # (3)
    logger.info(f"Starting job {jobname}")
    mod = importlib.import_module(mod_name)                 # (4)
    fn = getattr(mod, fn_name)                              # (5)
    fn()                                                    # (6)


# :cloak
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


# :endcloak
if __name__ == "__main__":
    _init_logging_system()
    main()
# :endsnippet
