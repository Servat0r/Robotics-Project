## Installation
First, intall POV-Ray: https://en.wikibooks.org/wiki/POV-Ray/Set_up.

## Setup
Then create directories to store .pov files and the rendered images.

`mkdir POV`

`mkdir images`

To cleanup after each trial, you can run:
`
rm POV/*; rm images/*
`
## Image generation
To generate the .pov files execute on terminal

`python single_section_cnn.py`

After this you will find generated files in the _POV/_ directory.

To render the frames from the .pov files run

`./render_frames.sh`

After this you will find generated images in the _images/_ directory.

## Video generation
`./make_video.sh`

## Convert video in gif
`ffmpeg -i video.mp4 video.gif`