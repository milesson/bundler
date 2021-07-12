import subprocess
import glob, os, re, getopt, sys

output_dir = os.getcwd()
output_file = 'output.mp4'
file_type = "*.png"
subdirectory_key = 'alpha'

# Commandline usage of the script
def usage():
    print ("Usage: -d 'directory' -o 'output file' -s 'subdirectory key' -t 'file type'")
    sys.exit(2)

# Returns a list of images from the input directory
def get_list_of_files(dir):
    file_list = []
    #os.chdir(dir)  # FIX THIS! Ugly
    print(os.path.join(dir,file_type))
    image_list = glob.glob(os.path.join(dir,file_type))
    #os.chdir(output_dir)
    image_list.sort(key=lambda var:[int(x) if x.isdigit() else x for x in re.findall(r'[^0-9]|[0-9]+', var)]) # Sort list by numbers
    for file in image_list:
        file_list.append(os.path.join(dir,file))
    return file_list

# Remove 1st argument from the list of command line arguments
argumentList = sys.argv[1:]
 
# Input options 
options = "hd:o:s:t:"
long_options = ["Help", "Directory=", "Output=", "SubDirKey=", "Filetype="]
 
try:
    # Parsing argument
    arguments, values = getopt.getopt(argumentList, options, long_options)  
     
    # checking each argument
    for currentArgument, currentValue in arguments:
 
        if currentArgument in ("-h", "--Help"):
            usage()    
             
        elif currentArgument in ("-d", "--Directory"):
            if os.path.isdir(currentValue):
                root_dir = currentValue
            else:
                print("Error: '" + currentValue + "' is not a valid directory!")
                usage()

        elif currentArgument in ("-o", "--Output"):
            output_file = currentValue

        elif currentArgument in ("-s", "--SubDirKey"):
            subdirectory_key = currentValue

        elif currentArgument in ("-t", "--FileType"):
            file_type = currentValue

except getopt.error as err:
    # output error, and return with an error code
    print (str(err))
    usage()

# Get list of directories
if(root_dir):
    sequences = glob.glob(root_dir+"/*")
else:
    usage() # Exit if no directory is set

tmp_media_file = open('list.txt', 'w+')

# loop trough all sequence directories
for dir in sequences:

    image_dir = glob.glob(dir+"/*"+subdirectory_key+"*")
    if (image_dir): ## FIX THIS (will not work if there is multiple subfolders)
        # Get list of sorted images in subdirectory
        file_list = get_list_of_files(image_dir[0])

        # Write list to temporary file
        for item in file_list:
            tmp_media_file.write("file '"+item+"'\n")

tmp_media_file.close()

if(os.path.getsize('list.txt') <= 0): 
    print("Error: No files found matching type '" + file_type + "'")
    sys.exit(2)

# Use list.txt to create ffmpeg video
subprocess.call(['ffmpeg','-r', '25', '-f', 'concat', '-safe', '0', '-i', \
     os.path.join(output_dir,"list.txt"), '-c:v', 'libx264', '-vf', 'fps=25', output_file])

# Remove temp file
os.remove('list.txt')