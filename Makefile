.PHONY: all

all: hxrss_main_window.py

%.py : %.ui
	pyuic5 -o $@ $<
