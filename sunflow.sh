#!/bin/sh

# Source functions library
. /usr/share/java-utils/java-functions

MAIN_CLASS=SunflowGUI

BASE_JARS="janino sunflow"
BASE_FLAGS="-Xmx810m"

# Set parameters
set_jvm
set_classpath $BASE_JARS
set_flags $BASE_FLAGS
set_options $BASE_OPTIONS

# Let's start
run "$@"
 
