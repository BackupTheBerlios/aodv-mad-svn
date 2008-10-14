#!/usr/bin/env python
#
# Copyright (C) 2008 GPLv2 kernel-labs.org
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
# Authors:
#   Javi Roman  <javiroman@kernel-labs.org>
'''RSU Tester

This example demonstrates the use of nomadic devices in 
Vehicular Ad-Hoc Networks (VANET).  Demonstrates the 
reception of Road Side Units messages from infrastructure.

'''
import gtk
import socket
import gobject
import os
import pango

IMAGEDIR = os.path.join(os.path.dirname(__file__), 'images')

IMAGE1 = os.path.join(IMAGEDIR, 'wifibutton.png')
IMAGE2 = os.path.join(IMAGEDIR, 'staticsbutton.png')
IMAGE3 = os.path.join(IMAGEDIR, 'connbutton.png')
IMAGE4 = os.path.join(IMAGEDIR, 'highway-480-531.jpg')

SIGIMG1 = os.path.join(IMAGEDIR, 'sig_60_t.gif')
SIGIMG2 = os.path.join(IMAGEDIR, 'sig_congestion_t.gif')
SIGIMG3 = os.path.join(IMAGEDIR, 'sig_luz_t.gif')
SIGIMG4 = os.path.join(IMAGEDIR, 'sig_noadelan_t.gif')

RSU1    = os.path.join(IMAGEDIR, 'rsu-1-font.gif')
RSU2    = os.path.join(IMAGEDIR, 'rsu-2-font.gif')
RSU3    = os.path.join(IMAGEDIR, 'rsu-3-font.gif')
GW1     = os.path.join(IMAGEDIR, 'gw1-font.gif')

class RsuTest (gtk.Window):
	
	__title_application = "RSU Tester"
	__RSU = 0
	__STATS = 1
	__CONNECT = 2
	buf = 102400

	def __init__(self, parent=None):
		# Create the toplevel window
		gtk.Window.__init__(self)
		try:
			self.set_screen(parent.get_screen())
		except AttributeError:
			self.connect('destroy', lambda *w: gtk.main_quit())

		self.set_title(self.__title_application)

		# Monitoring socket
		self.UDPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.UDPSock.bind(("localhost", 7777))
		gobject.io_add_watch(self.UDPSock, gobject.IO_IN, self.GetSocketIO_cb)
		
		vbox = gtk.VBox()

		self.mainNotebook = gtk.Notebook()
		self.mainNotebook.set_show_tabs(False)

		style = self.mainNotebook.get_style().copy()
		pixbuf = gtk.gdk.pixbuf_new_from_file(IMAGE4)
		pixmap, mask = pixbuf.render_pixmap_and_mask()
		style.bg_pixmap[gtk.STATE_NORMAL] = pixmap
		self.mainNotebook.set_style(style)     

		#
		# Notebook 1
		# 
                label = gtk.Label() # tab label
                frameAct = gtk.Frame("Road Side Units") # frame label
		frameAct.set_shadow_type(gtk.SHADOW_NONE)
		frameAct.set_label_align(0.5, 0.5)
		l = frameAct.get_label_widget()
		#l.modify_font(pango.FontDescription("Crackdown O1 BRK normal 20"))
		l.modify_font(pango.FontDescription("sans bold 10"))
                frameAct.set_border_width(5)
                self.mainNotebook.append_page(frameAct, label)
	
		table = gtk.Table(2, 2, True)
		frameAct.add(table)

		self.rsu1_img = gtk.Image()
		pixbuf = gtk.gdk.pixbuf_new_from_file(RSU1)
		self.rsu1_img.set_from_pixbuf(pixbuf)
		table.attach(self.rsu1_img, 0, 1, 0, 1, gtk.EXPAND|gtk.FILL)

		#b = gtk.Button("RSU-GW1")
		#b.set_border_width(10)
		#table.attach(b, 0, 1, 0, 1, gtk.EXPAND|gtk.FILL)

		self.rsu2_img = gtk.Image()
		pixbuf = gtk.gdk.pixbuf_new_from_file(RSU2)
		self.rsu2_img.set_from_pixbuf(pixbuf)
		table.attach(self.rsu2_img, 1, 2, 0, 1, gtk.EXPAND|gtk.FILL)

		self.rsu3_img = gtk.Image()
		pixbuf = gtk.gdk.pixbuf_new_from_file(RSU3)
		self.rsu3_img.set_from_pixbuf(pixbuf)
		table.attach(self.rsu3_img, 0, 1, 1, 2, gtk.EXPAND|gtk.FILL)

		self.gw1_img = gtk.Image()
		pixbuf = gtk.gdk.pixbuf_new_from_file(GW1)
		self.gw1_img.set_from_pixbuf(pixbuf)
		table.attach(self.gw1_img, 1, 2, 1, 2, gtk.EXPAND|gtk.FILL)

		#
		# Notebook 2
		# 
                label = gtk.Label()
                frameAct = gtk.Frame("VANET Statistics")
		frameAct.set_shadow_type(gtk.SHADOW_NONE)
		frameAct.set_label_align(0.5, 0.5)
		l = frameAct.get_label_widget()
		l.modify_font(pango.FontDescription("sans bold 10"))
                self.mainNotebook.append_page(frameAct, label)

		#
		# Notebook 3
		# 
                label = gtk.Label()
                frameAct = gtk.Frame("Connectivity")
		frameAct.set_shadow_type(gtk.SHADOW_NONE)
		frameAct.set_label_align(0.5, 0.5)
		l = frameAct.get_label_widget()
		l.modify_font(pango.FontDescription("sans bold 10"))
                self.mainNotebook.append_page(frameAct, label)

		#
		# Navigation Buttons
		# 
		hbox = gtk.HBox()

     		boton = gtk.EventBox()
		image = gtk.Image()
		image.set_from_file(IMAGE1)
		boton.add(image)
		tab = self.__RSU
		boton.set_events(gtk.gdk.BUTTON_PRESS_MASK)
		boton.connect("button_press_event", self.cambia_tab_cb, tab)
		hbox.pack_start(boton)

     		boton = gtk.EventBox()
		image = gtk.Image()
		image.set_from_file(IMAGE2)
		boton.add(image)
		tab = self.__STATS
		boton.set_events(gtk.gdk.BUTTON_PRESS_MASK)
		boton.connect("button_press_event", self.cambia_tab_cb, tab)
		hbox.pack_start(boton)

     		boton = gtk.EventBox()
		image = gtk.Image()
		image.set_from_file(IMAGE3)
		boton.add(image)
		tab = self.__CONNECT
		boton.set_events(gtk.gdk.BUTTON_PRESS_MASK)
		boton.connect("button_press_event", self.cambia_tab_cb, tab)
		hbox.pack_start(boton)

		self.mainNotebook.set_current_page(self.__RSU)
		vbox.pack_start(self.mainNotebook, True)
		vbox.pack_start(hbox, False)

		self.add(vbox)
		self.show_all()

	def cambia_tab_cb(self,  _a, _b, tab):
		self.mainNotebook.set_current_page(tab)

	def GetSocketIO_cb(self, a, b):
		data, addr = self.UDPSock.recvfrom(self.buf)
		if data == "GW1":
			pixbuf = gtk.gdk.pixbuf_new_from_file(SIGIMG4)
			self.gw1_img.set_from_pixbuf(pixbuf)	
		elif data == "RSU1":
			pixbuf = gtk.gdk.pixbuf_new_from_file(SIGIMG1)
			self.rsu1_img.set_from_pixbuf(pixbuf)	
		elif data == "RSU2":
			pixbuf = gtk.gdk.pixbuf_new_from_file(SIGIMG2)
			self.rsu2_img.set_from_pixbuf(pixbuf)	
		elif data == "RSU3":
			pixbuf = gtk.gdk.pixbuf_new_from_file(SIGIMG3)
			self.rsu3_img.set_from_pixbuf(pixbuf)	

		return True

def main():
	#gtk.rc_parse("./gtkrc")
	RsuTest()
	gtk.main()

if __name__ == '__main__':
	main()
