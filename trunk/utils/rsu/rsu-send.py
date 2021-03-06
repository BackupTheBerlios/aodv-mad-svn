#!/usr/bin/env python
#
# Copyright (C) 2008 Telefonica I+D (Spain)
#                                                                      
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.                             
#                                                                  
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
#   GNU General Public License for more details.                 
#                                                                 
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the
#   Free Software Foundation, Inc.,             
#   59 Temple Place - Suite 330, Boston, MA  02111-1307, USA. 
#
# This code has been developed within the context of the DRIVE 
# research project.
#
# Testing:  nc -l -u 7777 (listen incomming UDP connections)
#
# Authors:
#   Jessica Colom <jess2188@mit.edu>
#   Javi Roman  <javiroman@kernel-labs.org>
#   Jose A. Olivera <jaoo@tid.es>

import sys
import socket
import signal
import syslog
import time
import os

debug = 1 
end = 0

def daemonize():
    # do the UNIX double-fork magic, see Stevens' "Advanced
    # Programming in the UNIX Environment" for details (ISBN 0201563177)
    try:
        pid = os.fork()
        if pid > 0:
            # exit first parent
            sys.exit(0)
    except OSError, e:
        quote = 'broadpro: fork #1 failed: ' + e.errno + '(' + e.strerror + ')'
        syslog.syslog(quote)  
        sys.exit(1)

    # decouple from parent environment
    os.chdir("/")   #don't prevent unmounting....
    os.setsid()
    os.umask(0)

    # do second fork
    try:
        pid = os.fork()
        if pid > 0:
            # exit from second parent, print eventual PID before
            sys.exit(0)
    except OSError, e:
        quote = 'broadpro: fork #2 failed: ' + e.errno + '(' + e.strerror + ')'
        syslog.syslog(quote)  
        sys.exit(1)

def sigterm_handler(signum, frame):
    global end 

    if debug:
        quote = 'broadpro: Signal handler called with signal ' + str(signum)
        syslog.syslog(quote)
    end = 1    

def main():
    signal.signal(signal.SIGTERM, sigterm_handler)

    if len(sys.argv) == 5:

        addr = (sys.argv[1], int(sys.argv[2]))  # VANET broadcast address
        if debug:
            quote = 'broadpro: Sending broadcast messages to ' + addr[0] + ':' + str(addr[1])
            syslog.syslog(quote)

        # Create socket
        UDPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

        if hasattr(socket,'SO_BROADCAST'): # Broadcast socket
            UDPSock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        try:
            while end != 1:
                data = sys.argv[3]
		
		#for i in range(100):
		#	data = "message #" + str(i)
                #	UDPSock.sendto(data, addr)
	        #        time.sleep(0.1)

                UDPSock.sendto(data, addr)
                time.sleep(int(sys.argv[4]))

        except IOError:
            quote = 'IOError exception caught'
            syslog.syslog(quote)
  
        UDPSock.close()             # Close socket

    else:
        print "Usage: ./rus-send.py <vanet_broadcast_addr> <port> <message> <interval>"

if __name__ == "__main__":
    daemonize()
    main()
