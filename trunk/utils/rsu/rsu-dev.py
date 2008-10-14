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

def main():

    if len(sys.argv) == 5:

        addr = (sys.argv[1], int(sys.argv[2]))  # VANET broadcast address
        quote = 'broadpro: Sending broadcast messages to ' + addr[0] + ':' + str(addr[1])
	print quote
		
        # Create socket
        UDPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

        if hasattr(socket,'SO_BROADCAST'): # Broadcast socket
            UDPSock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        try:
		data = sys.argv[3]
		
		#for i in range(100):
		#	data = "message #" + str(i)
                #	UDPSock.sendto(data, addr)
	        #        time.sleep(0.1)

		UDPSock.sendto(data, addr)

        except IOError:
            quote = 'IOError exception caught'
            syslog.syslog(quote)
  
        UDPSock.close()             # Close socket

    else:
        print "Usage: ./rus-send.py <vanet_broadcast_addr> <port> <message> <interval>"

if __name__ == "__main__":
    main()
