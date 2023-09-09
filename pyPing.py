# -*- coding: utf-8 -*-
# Copyright 2023 WebEye
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import argparse
import logging
import os.path
import sys
import time
import re

from pythonping import ping
from io import StringIO


__VERSION__ = "1.0.1"

def main():
    parser = argparse.ArgumentParser(
      description='runner',
      epilog="That's all folks"
    )

    parser.add_argument('-t', '--target', dest='target', type=str, default='localhost')
    parser.add_argument('-to', '--timeout', dest='timeout', type=int, default=1)
    parser.add_argument('-lf', '--logfile', dest='log_file', type=str)
    parser.add_argument('-ll', '--loglevel', dest='log_level', type=str, default='INFO',
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'])
    parser.add_argument('-tp', '--template', dest='template', type=str, default='internet',
                        choices=['lan', 'internet'])
    parser.add_argument('-v', '--version', action='store_true')

    try:
        args = parser.parse_args()
    except SystemExit:
        sys.exit()

    if args.version:
        print(f'pyPing Version {__VERSION__}')
        sys.exit()

    _loggerExists = False
    if args.log_file is not None and len(args.log_file) > 0:
        directory = os.path.dirname(args.log_file)
        if not os.path.exists(directory):
            print('log path is not existing')
            sys.exit()
        else:
            _loggerExists = True

    if args.log_file is not None and len(args.log_file) > 0:
        _loggerExists = True
        _logger = logging.getLogger()
        _log_handler = logging.FileHandler(args.log_file)
        _str_log_level = args.log_level
        _log_level = getattr(logging, _str_log_level)
        _logger.setLevel(_log_level)
        _log_handler.setLevel(_log_level)

        _log_format = logging.Formatter('%(asctime)s - %(levelname)-8s - %(message)s')
        _log_handler.setFormatter(_log_format)

        _logger.addHandler(_log_handler)

    try:
        while True:
            _stdOut = StringIO()
            ping(target=args.target, count=1, verbose=True, out=_stdOut)
            line = _stdOut.getvalue().strip()

            result, pingtime = parse(line)
            output = f'ping {args.target}: {line}'
            if _loggerExists:
                if not result:
                    _logger.critical(output)
                else:
                    if args.template == 'lan':
                        if pingtime < 3.0:
                            _logger.debug(output)
                        elif pingtime < 6.0:
                            _logger.info(output)
                        elif pingtime < 20.0:
                            _logger.warning(output)
                        else:
                            _logger.error(output)
                    else:
                        if pingtime < 20.0:
                            _logger.debug(output)
                        elif pingtime < 50.0:
                            _logger.info(output)
                        elif pingtime < 100.0:
                            _logger.warning(output)
                        else:
                            _logger.error(output)

            print(output)
            if result:
                time.sleep(args.timeout)

    except KeyboardInterrupt:
        pass


def parse(line):
    if line == 'Request timed out':
        return False, None
    else:
        x = re.search('bytes in(.*)ms', line)
        tmp = re.sub('bytes in', '', x.group())
        tmp = re.sub('ms', '', tmp)
        return True, float(tmp)


if __name__ == "__main__":
    main()
