## Note: These instructions are currently being updated 

# Official development location for the Elixir Germline Variant Calling pipeline

## Genering instructions for running/testing outside TSD  

### Setup and preparations

The startFromDocker.sh script assumes that a certain folder structure is in place, and it is recommended that you use the same folder structure unless you want to edit the script manually to suit your own preferences.  
The simplest way to get started is to clone this repository, change the file paths as described below, install Docker and then you're good to go!  

To install Docker you can follow the appropriate instructions on Dockers website for instructions: https://docs.docker.com/engine/installation/

To install the latest rbFlow based Docker image, run 
```
sudo docker pull kjellptrsn/germlinevarcalldocker
```
(These instructions assume you are running docker through sudo, if you are a member of the docker group on your system, you setup may allow you to skip the sudo command).


Before we run the docker image, we need to configure the startFromDocker.sh script.  

Scroll down and change the file paths at "# Paths" to point to your reference files and the data folder (= the folder you checked out this repo to. Having data in a separate location to be tested and developed further next). 

The startFromDocker.sh script has divided the pre processing and germline variant calling steps into two separate scripts called preprocessing.yaml and germline_varcall.yaml. These scripts are stored in variables called "SCRIPT1" and "SCRIPT2" respectively. The script will both be run one after the other: SCRIPT2 after SCRIPT1 has completed.

If you would like to only run one of the scripts, you need to manually edit the startFromDocker.sh script and comment out either of these two lines: 
```
docker run -t --rm $CUST_USERID -v=$REFERENCE:/References -v=$DATA:/Data -w=/Data/ $IMAGE_ID sh -c "rbFlow.rb -c $SCRIPT1 -r"
docker run -t --rm $CUST_USERID -v=$REFERENCE:/References -v=$DATA:/Data -w=/Data/ $IMAGE_ID sh -c "rbFlow.rb -c $SCRIPT2 -r" 
```

### Run the workflow

As long as you run the startFromDocker.sh script from the "run" folder you should be ready to test the pipeline with the test data that is included in the "Samples" folder. Be adviced that the pipeline will crash on the final step in the germline_varcall.yaml workflow called "VariantRecalibration" due to too few read in the test fastq files (the variant quality recalibration steps will fail). As long as you have a complete set of fastq files the pipeline will finish successfully though.  
To start the pipeline, go to the terminal, change your working directory to the "run" directory and run 
```
sudo sh startFromDocker.sh
```


### Cleaning the folder between runs  
If you run the clean.sh script, you will delete everything that gets created during an analysis.  



## Instructions for Deployment and Running pipeline inside TSD

### Deployment of docker image in TSD Core Facility Docker VM

### Deployment of Workflow definitions and scripts needed

### How to run the workflow

```
sudo RunDockerWorkflow-TSD.py -i /absolute/path/to/inputs_dir/ -o /absolute/path/to/outputs_dir/ -r /absolute/path/to/references_dir/ -i /absolute/path/to/workflow_script.yaml
```

All directories and files have to be in your project area.

### Cleaning the data folder between runs
```
rm -r outputs_dir/*
```


### Restarting a run after an error

If you get an error, you can check the log file generated by the workflow located in the "***outputs_dir/Logs***" to find the failing step.
You can acces to logs from this step in the "***outputs_dir/step_dir/ToolName_stderr-Date-Time.log***"
After you have fixed the problem you can restart the workflow. The engine doesn't restart steps detected as succesfully passed, if you want restart a specific step you can remove "***outputs_dir/FinishedSteps/step_name.passed***"

### Logs

Usefull tips

Get all command exectuted by the workflow
```
grep EXECUTE outputs_dir/Logs/WorkFlowRun_Date_Time.log 
```

Get all running time for each steps
```
grep END: outputs_dir/Logs/WorkFlowRun_Date_Time.log 
```







