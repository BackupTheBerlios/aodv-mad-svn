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

buf = 102400

def main():
	# Create socket
	UDPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

	# bind the address to the socket 
	UDPSock.bind(("localhost", 7777))

	while 1:
		data, addr = UDPSock.recvfrom(buf)
		print data

if __name__ == "__main__":
	main()
