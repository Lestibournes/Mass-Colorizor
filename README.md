# Mass Colorizor

A commandline utility to search through a directory and convert all the colors according to the settings in a json config file. Non-destructive.

options:
--config=[file]: a json file specifying all the color conversions. Required.
--src=[file]: the root directory of the directory structure to be scanned. Required.
--dest=[file]: the root directory into which the files in src are to be copied. Required.
--colors=[file]: a json file listing color names and their corresponding rgb values in hex. Optional.

-r: make the scan recursive
--verbose: list all the conversions that take place and where they are
--search: list all the colors in the directory structure. Will not perform the conversion. When --search is specified then --config and --dest become optional.

This script was originally created for the purpose of changing the color schemes of themes. Although it seems to work as intended, the results need to be tweaked to be usable, especially since some graphics get the same color as the background and become invisible, but it still saves a lot of work over modifying hundreds or thousands of color strings manually.

Requires python 3.