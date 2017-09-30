# Item-Catalog

## What's this

This project is a web application that provides a list of libraries with a lot of books as well as provides a user registration and authentication system (Google signin). Registered users will have the ability to post, edit and delete their own items.


## How to use

### 1. Install the Virtual Machine
The PostgreSQL database and support software needed for this project are provided by a Linux virtual machine (VM). You have to install the VM first. You'll need to install tools called **Vagrant** and **VirtualBox** to install and manage VM.
#### (1) Use a terminal
For **Mac/Linux** systems, your regular terminal prgram will do just fine. For **Windows**, I recommend using **Git Bash** terminal that comes with the Git Software.
#### (2) Istall Vagrant
Download Vagrant from *vagrantup.com*, install the version for your operating system. If Vagrant is sucessfully installed, you will be able to run ```vagrant --version``` in your terminal to see the version number.
#### (3) Download the VM configuration
Download and unzip *FSND-Virtual-Machine.zip*. This will give you a directory called FSND-Virtual-Machine. Use ```cd``` command to navigate to the FSND-Virtual-Machine directory and use ```ls``` command to see the files in it.
#### (4) Start the VM
From your terminal, inside the **vagrant** subdirectory, run the command ```vagrant up```. This will cause vagrant to download Linux operating system and install it. When ```vagrant up``` is finished running, you will get your shell prompt back. At this point, you can run ```vagrant ssh``` to log into your newly installed Linux VM.
#### (5) Running the database
The PostgreSQL database server will automatically be started inside the VM. You can use ```psql``` command-line tool to access it and run SQL statements.
#### (6) Logging out and in
If you type ```exit``` or ```Ctrl+D``` at the shell prompt inside the VM, you will be logged out, and put back into your host computer's shell. To log back in, make sure you're in the same directory and type ```vagrant ssh``` again. If you reboot your computer, you will need to run ```vagrant up``` to restart the VM.



### 2. Run the python files
#### (1) vagrant path setup
Before you run the python files, make sure you are in the correct path in the vagrant shell. The shared directory is located at **/vagrant**. To access your shared files: ```cd /vagrant```. Make sure in the shared directory, you have all the project files.
#### (2) Database setup
In vagrant shell, use command ```python database_setup.py``` to set up the database which will be uesd in this application.
#### (3) Populate the database
In vagrant shell, use command ```python lotsofbooks_withusers.py``` to populate the database with libraries and books.
#### (4) Run the application
In vagrant shell, use command ```python item_catalog_project.py``` to run the web application. The application should run in port 8000. To access to the web page, type ```localhost:8000``` in your browser, then the web application should be there. Have fun creating your own libraries!

