## ------------------------
## Copyright. my-hpc-com
## Bob Peulen
## 2023
## ------------------------

########################################################################
######################################################################## Set Variables that are fixed in script
########################################################################

namespace = "frqap2zhtzbe"


########################################################################
######################################################################## Base imports and Environment variables
########################################################################

## Base Conda imports
# Importing only the conda / pip installs that are present in the base template. Any other package needs to be installed in the ran script

print("---------------------------------------------------------------")
print("Start Experiment")
print("Base imports")
import oci
import ads
import ocifs

## Fetch environment variables
print("Fetch the environment variables")
USER_NAME = os.environ.get("USER_NAME", "no_value")                ## input = user name in apex. Automatically passed. User name in apex is also main bucket name.
ENTRY_POINT = os.environ.get("ENTRY_POINT", "no_value")            ## input = file name. Example: main.py or entrypoint.py
FILES = os.environ.get("MAIN_BUCKET_NAME", "no_value")             ## input = list. Example: [example.csv, analyze_me.py, image_1.jpg, image_2.jpg]

print("Your user name is " + str(USER_NAME))
print("Your main entrypoint file is " + str(ENTRY_POINT))
print("Your additional files (if any) are " + str(FILES))

#Get job run ocid
JOB_RUN_OCID = os.environ.get('JOB_RUN_OCID', "UNDEFINED")

#define full input bucket and output bucket
full_input_bucket = "oci://" + USER_NAME + "@" + namespace + "/b_input_files/"
full_output_bucket = "oci://" + USER_NAME + "@" + namespace + "/b_output_files/"


########################################################################
######################################################################## Fetch entrypoint file and additional files from bucket and store locally
########################################################################

def get_files_from_input_bucket(full_input_bucket):
        
    #get the files from the bucket and store locally
    fs = ocifs.OCIFileSystem()
    
    #invalidate cache
    fs.invalidate_cache(full_input_bucket)
    
    #copy files
    all_files_in_bucket = fs.ls(full_input_bucket) #all files, including files that are not selected to run in experiment
    
    #fetch files
    fs.get(full_input_bucket, "./" , recursive=True, refresh=True)  #store files in the bucket in "./" in Job Block storage
    
    return all_files_in_bucket

#call function
all_files_in_bucket = get_files_from_input_bucket(full_input_bucket)

########################################################################
######################################################################## run entrypoint
########################################################################

print("Load and run your entrypoint file")
