import os

# Initializing the parent and directory
parent_dir = os.path.dirname(os.path.abspath(__file__))
print('Parent directory: ' + parent_dir)
target_dir = '/usr/share/mama'
print('Target directory: ' + target_dir)
# Checking target directory existence
if os.path.exists(target_dir):
    print('Target directory exists, so making it empty.')
    os.system("sudo rm -rf " + target_dir)
    os.system("sudo mkdir -p " + target_dir)
else:
    os.system("sudo mkdir -p " + target_dir)
    print('Target directory does not exist, so created.')

# Now copying files and folders
config_dir = parent_dir + '/config'
os.system("sudo cp -vr " + config_dir + " " + target_dir)
library_dir = parent_dir + '/library'
os.system("sudo cp -vr " + library_dir + " " + target_dir)
modules_dir = parent_dir + '/modules'
os.system("sudo cp -vr " + modules_dir + " " + target_dir)
resources_dir = parent_dir + '/resources'
os.system("sudo cp -vr " + resources_dir + " " + target_dir)
os.system("sudo cp -v " + parent_dir + "/mama.py" + " " + target_dir)
os.system("sudo cp -v " + parent_dir + "/mama-manager.py" + " " + target_dir)
os.system("sudo cp -v " + parent_dir + "/notifier.py" + " " + target_dir)

# Now copying desktop launcher
print('Now making desktop launcher.')
if os.path.exists('/usr/share/applications/mama.desktop'):
    os.system("sudo rm /usr/share/applications/mama.desktop")
    os.system(
        "sudo cp -v " + parent_dir + "/mama.desktop" + " /usr/share/applications")
else:
    os.system(
        "sudo cp -v " + parent_dir + "/mama.desktop" + " /usr/share/applications")

if os.path.exists('/usr/share/applications/mama-manager.desktop'):
    os.system("sudo rm /usr/share/applications/mama-manager.desktop")
    os.system("sudo cp -v " + parent_dir + "/mama-manager.desktop" + " "
                                                                     "/usr/share/applications")

print('\n\nInstalled Successfully.\n\n')
