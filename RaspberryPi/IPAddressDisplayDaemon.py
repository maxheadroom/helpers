#!/usr/bin/python
# -*- coding: utf-8 -*-

import daemon

import DisplayIPAddressDaemon 

with daemon.DaemonContext():
	DisplayIPAddressDaemon.display_ipaddr()