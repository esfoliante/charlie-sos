# This script should be ran on the first time
# that you run the whole project. 
#
# This already takes care of building the
# docker image as well as running it.

# This is a huge security risk, please make sure you
# don't have any malicious code in those .sh files
chmod +x *.sh

./build.sh
./start.sh
