#! /bin/env python

import os
import sys
import argparse
import subprocess



#--- Args ---

parser = argparse.ArgumentParser(description="Docker Workflow wrapper")
parser.add_argument("-i", "--input_folder",     type=str, required=True, help="The absolute path of the input  folder")
parser.add_argument("-o", "--output_folder",    type=str, required=True, help="The absolute path of the output folder")
parser.add_argument("-r", "--reference_folder", type=str, required=True, help="The absolute path of the references folder")
parser.add_argument("-y", "--yaml_file",        type=str, required=True, help="The absolute path of yaml recepe file of the workflow to run")
args = parser.parse_args()


#--- Functions ---

def get_project_path():
  path = os.getenv("HOME")
  path = os.path.normpath(path)
  pathArray = path.split(os.sep)
  return("/{0}/{1}/".format(pathArray[1],pathArray[2]))


def get_path_from_project(path):
  path = os.path.normpath(path)
  pathArray = path.split(os.sep)
  if "/{0}/{1}/".format(pathArray[1],pathArray[2]) == get_project_path():
    del pathArray[0]
    del pathArray[0]
    del pathArray[0]
    return "/".join(pathArray)
  else:
    print("path {0} need to be absolute and in your project area : {1}").format(path, get_project_path())
    exit()


def run_workflow(docker_command):
  process = subprocess.Popen(docker_command, close_fds=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  while process.poll() is None:
    out = process.stdout.read(1)
    sys.stdout.write(out)
    sys.stdout.flush()


def run_debug(command, docker_command):
  print("Command :")
  print(command)
  print("")
  print("Docker Command :")
  print(docker_command)
  print("")


def test_path(path):
  if os.path.isdir(path):
    return(True)
  else:
    print("Path {0} not found".format(path))
    exit()


def test_file(path):
  if os.path.isfile(path):
    return(True)
  else:
    print("Path {0} not found".format(path))
    exit()


def is_absolute(path):
  if os.path.isabs(path):
    return(True)
  else:
    print("Path {0} is not absolute".format(path))
    exit()


def get_uid():
  process = subprocess.Popen('id -u'.split(), stdout=subprocess.PIPE)
  output, error = process.communicate()
  return output.strip()


def get_gid():
  process = subprocess.Popen('id -g'.split(), stdout=subprocess.PIPE)
  output, error = process.communicate()
  return output.strip()


#--- parse pathes ---

input_path     = get_path_from_project(args.input_folder)
output_path    = get_path_from_project(args.output_folder)
reference_path = get_path_from_project(args.reference_folder)
yaml_path      = get_path_from_project(args.yaml_file)


#--- Test if path are valid ---

is_absolute(input_path)
is_absolute(output_path)
is_absolute(reference_path)
is_absolute(yaml_path)
test_path(input_path)
test_path(output_path)
test_path(reference_path)
test_file(yaml_path)


#--- Config ---

container_id    = 'kjellptrsn/germlinevarcalldocker:latest'

user_id         = get_uid()
group_id        = '2892' # p172-member-group
custom_user_id  = "-u={0}:{1}".format(user_id,group_id)
custom_env      = '-e HOME=/tmp' 


#--- Build the command running inside the container ---

command         = "\
ln -s /mnt/{0} /tmp/output && \
ln -s /mnt/{1} /tmp/input && \
ln -s /mnt/{2} /tmp/references && \
cd /tmp/ && \
rbFlow.rb -r -c /mnt/{3} \
".format(output_path, input_path, reference_path, yaml_path)


#--- Start the Container ---

docker_command  = "\
docker run -t --rm {0} {1} -v={2}:/mnt -w=/tmp {3} sh -c \"{4}\" \
".format(custom_env, custom_user_id, get_project_path(), container_id, command)


#--- Run ---

#run_debug(command, docker_command)
run_workflow(docker_command)



