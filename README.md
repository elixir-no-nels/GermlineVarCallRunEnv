## Note: These instructions are currently being updated 

# Official development location for the Elixir Germline Variant Calling pipeline

## Generic instructions for running/testing outside TSD  

### Setup and preparations

The Run-GermlineCalling.py script helps you to run the workflow in a Docker container with a minimal set of options. The workflow is divided in two parts, pre processing and germline calling described in two separate scripts called preprocessing.yaml and germline_varcall.yaml. You specify which script to run with the Run-GermlineCalling.py script.  

To install Docker you can follow the instructions on the Docker website: https://docs.docker.com/engine/installation/

Because the images is stored on a private repository you need to login ot the docker hub registrery.
```
sudo docker login
Password:[the password]
Login Succeeded
```

To install the latest rbFlow based Docker image, run 
```
sudo docker pull kjellptrsn/germlinevarcalldocker
```

You need to have been granted access to the kjellptrsn docker repository to be able to download the image. These instructions also assume you are running docker through sudo, but if you are a member of the docker group on your system, your setup may allow you to skip the sudo command.

### Instructions for downloading the reference files for this pipeline
The reference files are stored in the NeLS portal. You need to have been granted access to the _NCS_PM_Elixir_collaboration_ project folder to be able to download the reference files. If you have never used scp to download files from NeLS, watch [this tutorial](https://www.youtube.com/watch?v=TbUl8iuIwIw) for a guided walkthrough on how to download files from NeLS.  
Once you have your ssh private key file you can use the code below as a template, edit it and put in your NeLS username that you got in the tutorial. The NeLS file path should be the same as the one in the code below, and edit the destination file path by changing "/your/local/destination" to your actual folder where the reference files will be located.  

```
scp -r -i /path/to/your/keyfile/yourNeLSusername@nelstor0.cbu.uib.no.txt yourNeLSusername@nelstor0.cbu.uib.no:Projects/NCS-PM_Elixir_collaboration/Germline-varcall-wf-reference-files-v2.8/ /your/local/destination/
```
Or do it manually by logging in to the NeLS website and navigating to the _NCS_PM_Elixir_collaboration_ folder and download the reference files as a zip file.  

### How to configure the RunDockerWorkflow-local.py script

### How to run the workflow

You should be ready to test the pipeline with the test data that is included in the "Samples" folder now. Remember that when using the provided test data the pipeline will crash on the final step in the germline_varcall.yaml workflow called "VariantRecalibration" due to too few reads in the test fastq files (the variant quality recalibration steps will fail). As long as you have a complete set of fastq files the pipeline will finish successfully though.
This script take as parameters the input directory with samples, the output directory, the directory containing references, the yaml file descibing the workflow and the docker image id. In the log information displayed by this script you will find the shell command line used to start the workflow container.

# Pre-processing of samples
```
python RunDockerWorkflow-local.py -i path/input_folder -o path/output_folder -r path/reference_folder -y path/preprocessing.yaml -d kjellptrsn/germlinevarcalldocker
```

# variant calling
```
python RunDockerWorkflow-local.py -i path/input_folder -o path/output_folder -r path/reference_folder -y path/germline_varcall.yaml -d kjellptrsn/germlinevarcalldocker
```

### Cleaning the folder between runs  
If you run the clean.sh script, you will delete everything that gets created during an analysis.

### Deployment of docker image in TSD Core Facility Docker VM  

***This step to be performed by TSD, currently Abdulrahman and Ghislain both as the possibility to do this step.***

To install the latest rbFlow based Docker image:

1. Pull a fresh build of the docker to be installed to your local system first (NB: To be enhanced with two alternatives: dated tags for production releases from master branch, and testing/development images on the development branch)
```
sudo docker pull kjellptrsn/germlinevarcalldocker
```
You need to have been granted access to the kjellptrsn/germlinevarcalldocker docker repository to be able to download the image.  

2. Export a tar file of the docker image from your local system.

3. Import the tar file through the File Lock to the right TSD project internal disk. 

4. In the docker vm inside your tsd project (i.e. p172-docker-l), import the image from the tar file.  

### Instructions for downloading the reference files for this pipeline


***This step will be completed by Elixir-No staff***

The reference files are stored in the NeLS portal. You need to have been granted access to the _NCS_PM_Elixir_collaboration_ project folder to be able to download the reference files. If you have never used scp to download files from NeLS, watch [this tutorial](https://www.youtube.com/watch?v=TbUl8iuIwIw) for a guided walkthrough on how to download files from NeLS.  
Once you have your ssh private key file you can use the code below as a template, edit it and put in your NeLS username that you got in the tutorial. The NeLS file path should be the same as the one in the code below, and edit the destination file path by changing "/your/local/destination" to your actual folder where the reference files will be located.

```
scp -r -i /path/to/your/keyfile/yourNeLSusername@nelstor0.cbu.uib.no.txt yourNeLSusername@nelstor0.cbu.uib.no:Projects/NCS-PM_Elixir_collaboration/Germline-varcall-wf-reference-files-v2.8/ /your/local/destination/
```
The final step is to upload the reference files to your TSD project, follow [these instructions](http://www.uio.no/english/services/it/research/storage/sensitive-data/use-tsd/import-export/) for instructions on how to upload files to a TSD project.

For p172 the local reference location used is currently:
```
/tsd/p172/data/durable/varcall-workflow-testing/Germline-varcall-wf-reference-files-v2.8
```

***This has already been done***


This location of the reference files is critical and has to be updated/checked in the script configuration in the next step.  

### Deployment of Workflow definitions and scripts 

***This step will be prepared by Elixir-No staff, and completed by TSD staff (marked separately)***
 
1. Clone this repository to your local machine and then upload it to the TSD project with e.g sftp. Place the imported folder in a specific location, in p172 we use:
```
/tsd/p172/data/durable/varcall-workflow-testing/GermlineVarCallRunEnv
```

2. Next, we need to configure the Run-GermlineCalling.py script.  
Open the Run-GermlineCalling.py script with a text editor, scroll down and change the file paths at  
```"#--- Config ---"```  
to point to your reference files and preprocessing.yaml and germline_varcall.yaml files. This is the current locations to be used in p172:  
```
#--- Config ---
reference_folder  = get_path_from_project('/tsd/p172/data/durable/varcall-workflow-testing/Germline-varcall-wf-reference-files-v2.8')
prepros_yaml_file = get_path_from_project('/tsd/p172/data/durable/varcall-workflow-testing/GermlineVarCallRunEnv/preprocessing.yaml')
calling_yaml_file = get_path_from_project('/tsd/p172/data/durable/varcall-workflow-testing/GermlineVarCallRunEnv/germline_varcall.yaml')
``` 
***Elixir will edit the Run-GermlineCalling.py file in this location***  
3. ***TSD*** (Abdulrahman) then needs to make a copy of this script executable in the /usr/bin directory (without .py extension) and perform a test run to verify that it works properly.  
4. ***TSD***: The /usr/bin/Run-GermlineCalling needs to be allowed to run using sudo by all TSD-project members. This configuration is only needed at the very first deploy.


### How to run the workflow  
You should be ready to test the pipeline with the test data that is included in the "Samples" folder now. Remember that when using the provided test data the pipeline will crash on the final step in the germline_varcall.yaml workflow called "VariantRecalibration" due to too few reads in the test fastq files (the variant quality recalibration steps will fail). As long as you have a complete set of fastq files the pipeline will finish successfully though.  
You have three options when you run the pipeline. You can 1) run the preprocessing by using the "-p" flag, or 2) run germline variant calling by using the "-v" flag, or 3) run both of them by using both "-p -v". The example below would run the pipeline from the first to the last tool since it is using "-p -v".  
```
sudo Run-GermlineCalling -p -v -i path/to/inputs_dir/ -o path/to/outputs_dir/ 
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



