#Container ID

#1) Build with multithreading enabled
IMAGE_ID="kjellptrsn/germlinevarcalldocker:latest"

#User ID (Choose one of CUST_USERID definition)
USERID=`id -u`
GROUPID=`id -g`
#CUST_USERID="-u=501:501"
CUST_USERID="-u=$USERID:$GROUPID"

# Paths
REFERENCE="/your/local/path/to/Germline-varcall-wf-reference-files-v2.8"
DATA="/path/to/the/data/folder/that/contain/the/"Samples"/input/folder"


#Not used:
#CUST_ENV="-e HOME=/tmp"

# Workflow scripts to be executed (in working directory when no path present)
# Inputs defined as part of WF yaml, not parameterized
SCRIPT1="preprocessing.yaml"
SCRIPT2="germline_varcall.yaml"

# For Debug
#docker run -ti --rm $CUST_USERID -v=$REFERENCE:/References -v=$DATA:/Data -w=/Data/ $IMAGE_ID bash
# Start without --rm to be able to commit changes of image
#docker run -ti $CUST_USERID -v=$REFERENCE:/References -v=$DATA:/Data -w=/Data/ $IMAGE_ID bash

# For Running
docker run -t --rm $CUST_USERID -v=$REFERENCE:/References -v=$DATA:/Data -w=/Data/ $IMAGE_ID sh -c "rbFlow.rb -c $SCRIPT1 -r"
docker run -t --rm $CUST_USERID -v=$REFERENCE:/References -v=$DATA:/Data -w=/Data/ $IMAGE_ID sh -c "rbFlow.rb -c $SCRIPT2 -r"


# ---Special Instruction for OSX ---
# Because the disk space of the Docker host is from the Virtual machine that run Docker and not from OSX
# You need to import a Volume of OSX inside the vistual machine to be able to acces to this disk space from inside a container.
# A way to do that is Docker-machine-NFS, a script that create a NFS mount point from OSX inside the Boot2Docker virtual machine.
#
# Install docker-machine-nfs :
# https://github.com/adlogix/docker-machine-nfs
#
# Share a path /XXX/YYY between OSX and The boot2docker virtual machine
# docker-machine-nfs default --shared-folder=/XXX/YYY
