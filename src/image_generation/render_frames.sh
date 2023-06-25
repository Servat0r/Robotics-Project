#!/bin/bash

# parallel version based on https://unix.stackexchange.com/questions/103920/parallelize-a-bash-for-loop
# Set up working variables
POV_DIR=$PWD/POV
IMAGE_DIR=$PWD/images
STARTFOLDER=$PWD
IMAGES=$PWD/images

# Prepare image folder
cd $IMAGE_DIR


# In all povray files replace the default include file with the appropriate one
#SEDSTRING=s/scenepovray/${SCENENAME}/g
#sed -ie ${SEDSTRING} *.pov


task(){
	echo "Processing $f file..."

	filenameOnly=${f##*/}
	filenameNoExt=${filenameOnly%.*}
	echo $filenameNoExt
	echo $filenameOnly

	## Select your preferred resolution
	#povray -H200 -W320 Quality=11 Antialias=on $f Display=False
	#povray -H480 -W720 Quality=11 Antialias=on $f Display=False
	#povray -H720 -W1280 Quality=11 Antialias=on $f Display=False
	#povray -H1080 -W1920 Quality=11 Antialias=on $f Display=False # tipico 16:9
	povray -H540 -W960 Quality=11 Antialias=on $f Display=False
 	
 	mv $POV_DIR/$filenameNoExt.png $IMAGE_DIR
}

# Increasing N runs the loop in parallel
N=8
(
# Loop over all povray files and produce images
for f in $POV_DIR/**_rod.pov
do
   ((i=i%N)); ((i++==0)) && wait
   task & 
done
)

wait

# Go back to original folder
cd $STARTFOLDER
#mv $POV_DIR/**.png $IMAGE_DIR

