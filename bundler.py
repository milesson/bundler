#from posixpath import join
import subprocess
import glob, os, re
from typing import Sequence

ffmpeg = "/bin/ffmpeg"
root_dir = "/mnt/c/Users/DanielMilesson/Documents/repos/imgs"
output_dir = os.getcwd()
file = open('list.txt', 'w+')

# Returns a list of images from the input directory
def get_list_of_files(dir):
    file_list = []
    os.chdir(dir)  # FIX THIS!
    image_list = glob.glob("*.png")
    os.chdir(output_dir)
    image_list.sort(key=lambda var:[int(x) if x.isdigit() else x for x in re.findall(r'[^0-9]|[0-9]+', var)]) # Sort list by numbers
    for file in image_list:
        file_list.append(os.path.join(dir,file))
    return file_list


# Get list of directories
sequences = glob.glob(root_dir+"/*")

for dir in sequences:

    image_dir = glob.glob(dir+"/*alpha*")
    if (image_dir):
        # Get list of sorted images
        file_list = get_list_of_files(image_dir[0])
    else:
        continue

    # Write list to file
    for item in file_list:
        file.write("file '"+item+"'\n")

file.close()

# Use list to create ffmpeg video
subprocess.call([ffmpeg,'-r', '25', '-f', 'concat', '-safe', '0', '-i', os.path.join(output_dir,"list.txt"), '-c:v', 'libx264', '-vf', 'fps=25',  'out.mp4'])


#my_frame = 3
#subprocess.call([ffmpeg, '-r', '10', '-i', 'frame%03d.png' % my_frame,
#    ['-r',  'ntsc', 'movie%03d.mpg' % my_frame])
