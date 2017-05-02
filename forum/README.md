## Launching the Forum

### Prerequisites
* Follow the main instructions to launch your Virtual Machine and successfully log in via the `vagrant ssh` command

### Running the Forum
* Once logged in via SSH access shared files at `cd /vagrant`
* Use `ls` to view files in the current directory, the forum directory should be present.
* Type `cd /vagrant/forum` to change into the forum directory project files.
* Use `ls` to view files in the forum directory and check if the `forum.py` file exists.
* If it does exist, run `python forum.py` to serve on localhost.
* View on browser by typing served localhost into URL - eg. http://localhost:8000/)