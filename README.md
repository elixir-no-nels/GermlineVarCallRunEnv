## Note: These instructions are currently being updated 

# Official development location for the Elixir Germline Variant Calling pipeline

## Generic instructions for running/testing outside TSD  

### Setup and preparations

The Run-GermlineCalling.py script helps you to run the workflow in a Docker container with a minimal set of options. The workflow is divided in two parts, pre processing and germline calling described in two separate scripts called preprocessing.yaml and germline_varcall.yaml. You specify which script to run with the Run-GermlineCalling.py script.  

To install Docker you can follow the instructions on the Docker website: https://docs.docker.com/engine/installation/

To install the latest rbFlow based Docker image, run 
```
sudo docker pull kjellptrsn/germlinevarcalldocker
```
You need to have been granted access to the kjellptrsn docker repository to be able to download the image. These instructions also assume you are running docker through sudo, but if you are a member of the docker group on your system, your setup may allow you to skip the sudo command.

### Instructions for downloading the reference files for this pipeline
The reference files are stored in the NeLS portal. You need to have been granted access to the _NCS_PM_Elixir_collaboration_ project folder to be able to download the reference files. If you have never used scp to download files from NeLS, watch [this tutorial](https://www.youtube.com/watch?v=TbUl8iuIwIw) for a guided walkthrough on how to download files from NeLS.  
Once you have your ssh private key file you can use the code below as a template, edit it and put in your NeLS username that you got in the tutorial. The NeLS file path should be the same as the one in the code below, and edit the destination file path by changing "/your/local/destination" to your actual folder where the reference files will be located.  

```
scp -r -i yourNeLSusername@nelstor0.cbu.uib.no.txt yourNeLSusername@nelstor0.cbu.uib.no:Projects/NCS-PM_Elixir_collaboration/Germline-varcall-wf-reference-files-v2.8/ /your/local/destination/
```
Or do it manually by logging in to the NeLS website and navigating to the _NCS_PM_Elixir_collaboration_ folder and download the reference files as a zip file.  

### How to configure the Run-GermlineCalling.py script
Before we run the docker image, we need to configure the Run-GermlineCalling.py script.  

Open the Run-GermlineCalling.py script with a text editor and scroll down and change the file paths at 

```"#--- Config ---"```  
to point to your reference files and the preprocessing.yaml and germline_varcall.yaml files.  
### How to run the workflow

You should be ready to test the pipeline with the test data that is included in the "Samples" folder now. Remember that when using the provided test data the pipeline will crash on the final step in the germline_varcall.yaml workflow called "VariantRecalibration" due to too few reads in the test fastq files (the variant quality recalibration steps will fail). As long as you have a complete set of fastq files the pipeline will finish successfully though.  
You have three options when you run the pipeline. You can 1) run the preprocessing by using the "-p" flag, or 2) run germline variant calling by using the "-v" flag, or 3) run both of them by using both "-p -v". The example below would run the pipeline from start to finish since it is using "-p -v".
```
python Run-GermlineCalling.py -i /absolute/path/to/inputs_dir/ -o /absolute/path/to/outputs_dir/ -p -v

```

### Cleaning the folder between runs  
If you run the clean.sh script, you will delete everything that gets created during an analysis.

## Instructions for Deployment and Running pipeline inside TSD

### Deployment of docker image in TSD Core Facility Docker VM  
To install the latest rbFlow based Docker image, run 
```
sudo docker pull kjellptrsn/germlinevarcalldocker
```
You need to have been granted access to the kjellptrsn docker repository to be able to download the image.  
***Ghislain, could you fill out the rest about how to tar the image and upload it to a TSD project VM?***  

### Instructions for downloading the reference files for this pipeline
The reference files are stored in the NeLS portal. You need to have been granted access to the _NCS_PM_Elixir_collaboration_ project folder to be able to download the reference files. If you have never used scp to download files from NeLS, watch [this tutorial](https://www.youtube.com/watch?v=TbUl8iuIwIw) for a guided walkthrough on how to download files from NeLS.  
Once you have your ssh private key file you can use the code below as a template, edit it and put in your NeLS username that you got in the tutorial. The NeLS file path should be the same as the one in the code below, and edit the destination file path by changing "/your/local/destination" to your actual folder where the reference files will be located.

```
scp -r -i yourNeLSusername@nelstor0.cbu.uib.no.txt yourNeLSusername@nelstor0.cbu.uib.no:Projects/NCS-PM_Elixir_collaboration/Germline-varcall-wf-reference-files-v2.8/ /your/local/destination/
```
The final step is to upload the reference files to your TSD project, follow [these instructions](http://www.uio.no/english/services/it/research/storage/sensitive-data/use-tsd/import-export/) for instructions on how to upload files to a TSD project.  
***This has already been done***

### Deployment of Workflow definitions and scripts  
Clone this repository to your local machine and then upload it to the TSD project with e.g sftp. Before we run the docker image, we need to configure the Run-GermlineCalling.py script.  

Open the Run-GermlineCalling.py script with a text editor, scroll down and change the file paths at 

```"#--- Config ---"```  
to point to your reference files and preprocessing.yaml and germline_varcall.yaml files.  
***Elixir will edit the Run-GermlineCalling.py file, Abdulrahman, you need to make it executable in the /usr/bin directory and perform a test run to verify that it works properly.***

### How to run the workflow  
You should be ready to test the pipeline with the test data that is included in the "Samples" folder now. Remember that when using the provided test data the pipeline will crash on the final step in the germline_varcall.yaml workflow called "VariantRecalibration" due to too few reads in the test fastq files (the variant quality recalibration steps will fail). As long as you have a complete set of fastq files the pipeline will finish successfully though.  
You have three options when you run the pipeline. You can 1) run the preprocessing by using the "-p" flag, or 2) run germline variant calling by using the "-v" flag, or 3) run both of them by using both "-p -v". The example below would run the pipeline from the first to the last tool since it is using "-p -v".  
```
sudo Run-GermlineCalling.py -i /absolute/path/to/inputs_dir/ -o /absolute/path/to/outputs_dir/ -p -v
```

All directories and files have to be in your project area.  

### Cleaning the data folder between runs
```
rm -r outputs_dir/*
```

### Restarting a run after an error

If you get an error, you can check the log file generated by the workflow located in the "***outputs_dir/Logs***" to find the failing step.
You can access logs from this step in the "***outputs_dir/step_dir/ToolName_stderr-Date-Time.log***"
After you have fixed the problem you can restart the workflow. The engine doesn't restart steps detected as succesfully passed, if you want to restart a specific step you can remove "***outputs_dir/FinishedSteps/step_name.passed***"

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







