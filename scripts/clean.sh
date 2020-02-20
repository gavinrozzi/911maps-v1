#!/bin/bash
# This script will clean Active911 call data so that it can be loaded into 911maps
CSV_FILE=$1
# Change the offset (-0400)based upon your timezone
sed -i -E 's,([0-9]{2})/([0-9]{2})/([0-9]{4}),\3-\2-\1,g' $CSV_FILE
# TODO: The second line of this script ruins the data. It needs to be fixed. Right now just manually remove the EDT in Excel.
#sed -i '/EDT/d' $CSV_FILE
