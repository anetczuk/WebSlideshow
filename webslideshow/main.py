#!/usr/bin/python

# MIT License
# 
# Copyright (c) 2017 Arkadiusz Netczuk <dev.arnet@gmail.com>
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
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
    
    providerClass = MainWindow.import_module( "webslideshow/provider/" + args.provider )
    
    provider = providerClass( randomMode )              ## call constructor
    
    mainW = MainWindow.MainWindow(not args.nofs)
    mainW.setProvider( provider )
    mainW.setDisplayTime( args.dtime )
    mainW.main()
    