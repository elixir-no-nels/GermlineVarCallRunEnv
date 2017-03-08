#! /bin/env python

import os
import pwd
import sys
import argparse
import subprocess



#--- Args ---

parser = argparse.ArgumentParser(description="Docker Workflow wrapper")
parser.add_argument("-i", "--input_folder",     type=str, required=True, help="The absolute path of the input  folder")
parser.add_argument("-o", "--output_folder",    type=str, required=True, help="The absolute path of the output folder")
parser.add_argument("-r", "--reference_folder", type=str, required=True, help="The absolute path of the references folder")
parser.add_argument("-y", "--yaml_file",        type=str, required=True, help="The absolute path of yaml recepe file of the workflow to run")
parser.add_argument("-d", "--docker_image",     type=str, required=True, help="The docker images to use")
args = parser.parse_args()


#--- Functions ---

def run_workflow(docker_command):
  process = subprocess.Popen(docker_command, close_fds=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  while process.poll() is None:
    out = process.stdout.read(1)
    sys.stdout.write(out)
    sys.stdout.flush()


def run_debug(command, docker_command):
  #print("Command :")
  #print(command)
  #print("")
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
  # return the original user id even after sudo, in python
  user = os.environ['SUDO_USER'] if 'SUDO_USER' in os.environ else os.environ['USER']
  user_id  = pwd.getpwnam(user).pw_uid
  return(user_id)


def get_gid():
  process = subprocess.Popen('id -g'.split(), stdout=subprocess.PIPE)
  output, error = process.communicate()
  return output.strip()


#--- parse pathes ---

input_path     = args.input_folder
output_path    = args.output_folder
reference_path = args.reference_folder
yaml_path      = args.yaml_file


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

container_id    = args.docker_image

user_id         = get_uid()
group_id        = get_gid()
custom_user_id  = "-u={0}:{1}".format(user_id,group_id)
custom_env      = '-e HOME=/tmp' 


#--- Build the command running inside the container ---

command         = "\
cd /tmp/ && \
rbFlow.rb -r -c /tmp/workflow.yaml \
"


#--- Start the Container ---

docker_command  = "\
docker run -t --rm {0} {1} -v={2}:/tmp/output -v={3}:/tmp/input -v={4}:/tmp/references -v={5}:/tmp/workflow.yaml -w=/tmp {6} sh -c \"{7}\" \
".format(custom_env, custom_user_id, output_path, input_path, reference_path, yaml_path, container_id, command)


#--- Run ---

run_debug(command, docker_command)
run_workflow(docker_command)



