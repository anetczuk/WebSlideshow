#!/usr/bin/python

#
# <one line to give the library's name and an idea of what it does.>
# Copyright (C) 2017  Arkadiusz Netczuk <dev.arnet@gmail.com>
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
#


import logging
import argparse
import MainWindow


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Display internet gallery.')
    parser.add_argument('--provider', action='store', default="Demotywatory", help='Load given image provider' )
    parser.add_argument('--random', action='store_const', const=True, default=False, help="Gallery random mode (if supporting)" )
    parser.add_argument('--dtime', action='store', default=10, help="Display time of single image [s]" )
    parser.add_argument('--nofs', action='store_const', const=True, default=False, help='No fullscreen at startup' )
    parser.add_argument('--loglevel', action='store', help='Set log level' )

    args = parser.parse_args()
        
    if args.loglevel:
        llevel = getattr(logging, args.loglevel)
        logging.basicConfig(level=llevel)
    
    logging.info("Args: %s", args)
    
    if args.loglevel:
        print "Log level:", args.loglevel
    
    randomMode = args.random
    
    logging.info("Loading provider: %s", args.provider)
    
    providerClass = MainWindow.import_module( "provider/" + args.provider )
    
    provider = providerClass( randomMode )              ## call constructor
    
    mainW = MainWindow.MainWindow(not args.nofs)
    mainW.setProvider( provider )
    mainW.setDisplayTime( args.dtime )
    mainW.main()
    