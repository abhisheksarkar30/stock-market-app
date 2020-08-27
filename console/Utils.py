import importlib
import pkgutil
import os
import shutil
import subprocess
import sys
import matplotlib.pyplot as plt
from distutils import dir_util
from datetime import datetime


# Copy each file or all files recursively from a folder
def copy(src, destination_dir):
    try:
        if os.path.isfile(src):
            shutil.copy(src, destination_dir)
        else:
            dir_util.copy_tree(src, destination_dir)
    except Exception as e:
        print("Unable to copy: " + str(e))


# Create dir if doesn't exist
def create_dir(destination_dir):
    if not os.path.exists(destination_dir):
        try:
            os.makedirs(destination_dir)
        except Exception as e:
            print("Unable to create target dir: " + str(e))
            sys.exit(-1)


# Calls the specified python class in a subprocess
def script_invoker(script, args):
    return subprocess.getoutput(script + ".py " + " ".join(args))


# Import module dynamically
def fetch_module(module):
    return importlib.import_module(module)


# Get list of modules in a directory
def load_all_modules_from_dir(directory):
    module_list = []
    directory = sys.path[0] + "/" + directory
    for importer, package_name, _ in pkgutil.iter_modules([directory]):
        if package_name not in sys.modules:
            module_list.append(importer.find_module(package_name).load_module(package_name))
    return module_list


# Read lines from a file into a list
def file_reader(file_name):
    try:
        file = open(sys.path[0] + "/" + file_name, "r")
        lines = file.readlines()
        # Check for empty file
        if not lines:
            raise ValueError("No content found")
    except (FileNotFoundError, ValueError) as e:
        print("Unable to load file: " + str(e))
        sys.exit(-1)
    return lines


# Execute specified command in a subprocess
def execute_command(command):
    return subprocess.getoutput(command) if isinstance(command, str) else subprocess.check_output(command)


# Divides a list in chunks of specified size
def divide_chunks(source_list, chunk_size):
    # looping till end of list
    for index in range(0, len(source_list), chunk_size):
        yield source_list[index:index + chunk_size]


def get_date_from_string(date_string):
    return datetime.strptime(date_string, '%Y-%m-%d')


def get_month_year_from_string(date_string):
    return datetime.strptime(date_string, '%Y-%m')


def plot_graph(plot_type, data):
    plt.style.use('fivethirtyeight' if plot_type is None else str(plot_type))
    data['Close'].plot()
    plt.show()

