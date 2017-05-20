# Using a Virtual Machine w/ Relational Database
==============================================

## Description
A project set up to use a virtual machine (VM) to run an SQL database server and a web app that uses it.
The VM is a Linux server system that runs on top of your own computer.
* We can share files easily between our computer and the VM
* We'll be running a web service inside the VM which we'll be able to access from our regular browser locally.

We're using tools called Vagrant and VirtualBox to install and manage the VM. You'll need to install these to do some of the exercises.

## Prerequisites -
* We'll be using a Unix-style terminal on your computer. On Windows, we recommend using the Git Bash terminal that comes with the Git software (www.git-scm.com).
* For Windows users, you may use putty (http://www.chiark.greenend.org.uk/~sgtatham/putty/) for SSH implementation.

## Instructions
* VirtualBox is the software that actually runs the virtual machine. Install VirtualBox - (https://www.virtualbox.org/wiki/Downloads).
* Vagrant is the software that configures the VM and lets you share files between your host computer and the VM's filesystem. Install Vagrant - (https://www.vagrantup.com/downloads.html).
 * To find out if vagrant has successfully installed type `vagrant --version` into git bash or cmd

## Configure the VM
* Use Github to fork and clone or download the the repository - https://github.com/udacity/fullstack-nanodegree-vm.
* Once you download the files and end up with a new local directory containing the VM files.
 * Change to this directory in your terminal with cd.
 * Inside, you will find another directory called vagrant. Change directory to the vagrant directory.

### Start the Virtual Machine
* Inside the vagrant subdirectory, run the command `vagrant up`
 * This will cause Vagrant to download the Linux operating system and install it. This may take quite a while (many minutes) depending on how fast your Internet connection is.
* Once you get your shell prompt back. Run `vagrant ssh` to log in to your newly installed Linux VM
 * If you have trouble with an SSH client you may use the authentication information provided and use Putty to explore the VM via SSH

#### My Authentication Info
* Host: 127.0.0.1
* Port: 2222
* config.ssh.username = "ubuntu"
* config.ssh.password = "55562eefdc557c810fbaca5f"
* Private key: C:/Users/Christiaan/PhpstormProjects/Udacity Full Stack Nanodegree/Setting up VM/fullstack-nanodegree-vm/vagrant/.vagrant/machines/default/virtualbox
/private_key

### Running the Database
* The PostgreSQL database server will automatically be started inside the VM.
 * Run `psql` inside the VM command-line tool to access it and run SQL statements: eg. `select 2 + 2 as sum;`

### Logging out and in
* Run `vagrant reload` if you edit the Vagrant file or make other changes to code that would affect the virtual machine.
* If you type `exit` (or `Ctrl-D`) at the shell prompt inside the VM, you will be logged out, and put back into your host computer's shell. To log back in, make sure you're in the same directory and type `vagrant ssh` again.
* To exit Vagrant after the test simply type `logout`
* To stop Vagrant running in the background when done type `vagrant halt`
* If you reboot your computer, you will need to run `vagrant up` to restart the VM.


### Resources
* Udacity FSND Webcast on setting up Vagrant - https://www.youtube.com/watch?v=djnqoEO2rLc
