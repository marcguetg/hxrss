.PHONY: all

all: hxrss_main_window.py

# Remark: to edit the GUI, run 'designer'
#
# 2022-02-22: on xfeluser1, change the environment as follows:
# export PATH=/opt/anaconda/bin:$PATH
# (path from /home/xfeloper/released_software/scripts/pylaunch )
designer:
	designer hxrss_main_window.ui

%.py : %.ui
	pyuic5 -o $@ $<
