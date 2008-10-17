#!/usr/bin/env python
# WiFi proof of concepts.

import socket
import struct

class Iwstruct(object):
    """basic class to handle iwstruct data """
    
    def __init__(self):
        self.idx = 0
        self.sockfd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def parse_data(self, fmt, data):
        """ unpacks raw C data """
        size = struct.calcsize(fmt)
        idx = self.idx

        datastr = data[idx:idx + size]
        self.idx = idx+size
        value = struct.unpack(fmt, datastr)

        # take care of a tuple like (int, )
        if len(value) == 1:
            return value[0]
        else:
            return value
    
    def pack(self, fmt, *args):
        """ calls struct.pack and returns the result """
        return struct.pack(fmt, *args)

    def pack_wrq(self, buffsize):
        """ packs wireless request data for sending it to the kernel """
        # Prepare a buffer
        # We need the address of our buffer and the size for it. The
        # ioctl itself looks for the pointer to the address in our
        # memory and the size of it.
        # Dont change the order how the structure is packed!!!
        buff = array.array('c', '\0'*buffsize)
        caddr_t, length = buff.buffer_info()
        datastr = struct.pack('Pi', caddr_t, length)
        return buff, datastr
    
    def pack_test(self, string, buffsize):
        """ packs wireless request data for sending it to the kernel """
        buffsize = buffsize - len(string)
        buff = array.array('c', string+'\0'*buffsize)
        caddr_t, length = buff.buffer_info()
        s = struct.pack('Pii', caddr_t, length, 1)
        return buff, s

    def unpack(self, fmt, packed_data):
        """ unpacks data with given format """
        return struct.unpack(fmt, packed_data)

    def _fcntl(self, request, args):
        return fcntl.ioctl(self.sockfd.fileno(), request, args)
    
    def iw_get_ext(self, ifname, request, data=None):
        """ read information from ifname """
        # put some additional data behind the interface name
        if data is not None:
            buff = pythonwifi.flags.IFNAMSIZE-len(ifname)
            ifreq = ifname + '\0'*buff
            ifreq = ifreq + data
        else:
            ifreq = (ifname + '\0'*32)

        try:
            result = self._fcntl(request, ifreq)
        except IOError, (i, e):
            return i, e

        return (0, result[16:])

    def getMAC(self, packed_data):
        """ extracts mac addr from packed data and returns it as str """
        mac_addr = struct.unpack('xxBBBBBB', packed_data[:8])
        return "%02X:%02X:%02X:%02X:%02X:%02X" % mac_addr

def main():
       wstruct = Iwstruct() 

if __name__ == '__main__':
        main()

