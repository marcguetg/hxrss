.PHONY: all

all: hxrss_main_window.py

# remark: to edit the GUI, run 'designer'
designer:
	designer hxrss_main_window.ui

%.py : %.ui
	pyuic5 -o $@ $<
