A Vagrant Demo For EBRC Website Development
===========================================

This is an very incomplete starter project for EBRC website development. Copy it, make it your own, commit it to your own repository.

The Vagrant box has been provisioned using a subset of the same pipelines used to set up development webservers in the datacenter so it should have high parity with the traditional work environments. Nonetheless, treat this Vagrant project and box as a proof of concept and chance to identify features needed in our next generation VM templates.

Prerequisites
=====

Vagrant
---------------

Vagrant manages the lifecycle of the virtual machine, guided by the instructions in the `Vagrantfile` included with this project.

[https://www.vagrantup.com/downloads.html](https://www.vagrantup.com/downloads.html)

You should refer to Vagrant documentation and related online forums for information not covered in this document.

VirtualBox
------------------

Vagrant needs VirtualBox to host the virtual machine defined in this project's `Vagrantfile`. Other virtualization software (e.g. VMWare) are not compatible with this Vagrant project as it is currently configured.

[https://www.virtualbox.org/wiki/Downloads](https://www.virtualbox.org/wiki/Downloads)

You should refer to VirtualBox documentation and related online forums for information not covered in this document.

Ansible
---------------

_Ansible is currently not required. This is needed for the optional task of provisioning a specific website._

[http://docs.ansible.com/ansible/intro_installation.html](http://docs.ansible.com/ansible/intro_installation.html)

You should refer to Ansible documentation and related online forums for information not covered in this document.

The Ansible provisioner runs `ansible-galaxy` to acquire roles specified in `ansible/requirements.yml`. This step overwrites existing roles and any development edits you've made. Touch a `nogalaxy` file in the same directory as `Vagrantfile` to disable the `ansible-galaxy` step so your edits don't get deleted.

Vagrant Landrush Plugin (Optional)
--------------------------------------

The [Landrush](https://github.com/phinze/landrush) plugin for Vagrant provides a local DNS so you can register guest hostnames and refer to them in the host browser. It is not strictly required but it makes life easier than editing `/etc/hosts` files. This plugin has maximum benefit for OS X hosts, some benefit for Linux hosts and no benefit for Windows. Windows hosts will need to edit `hosts` files.

    vagrant plugin install landrush

_If you have trouble getting the host to resolve guest hostnames through landrush try clearing the host DNS cache by running_ `sudo killall -HUP mDNSResponder`.

If you want to host multiple product sites - say, sa.vm.toxodb.org and sa.vm.giardiadb.org - you may want our Landrush fork that supports multiple TLD management. Until and unless our [Pull Request](https://github.com/phinze/landrush/pull/125) is accepted by the upstream maintainer you will have to install the plugin using the gem file included with this project.

    vagrant plugin install landrush-0.18.0.gem

To manually build and install from source

    git clone https://github.com/mheiges/landrush.git
    cd landrush
    rake build
    vagrant plugin install pkg/landrush-0.18.0.gem

You should refer to Landrush and Vagrant documentation and related online forums for information not covered in this document.

Usage
=======

Clone This Vagrant Project
--------------------------

    clone https://github.com/mheiges/vagrant-webdev-poc.git

    cd vagrant-webdev-poc

Optionally prepare for automated website provisioning
-----------------

_This is still under development and highly experimental._

Copy `installsite_min.prop` from https://github.com/mheiges/ansible-ebrcwebsite/tree/master/doc to `installsite.prop` in the same directory as this project's `Vagrantfile`.

Edit `installsite.prop`. Configure a source for default values from /dashboard and other personalized settings.


Start the Virtual Machine
-------------------------

    vagrant up

ssh to the Virtual Machine
-----------------

To connect to the VM as the `vagrant` user, run

    vagrant ssh

Manually install a website
-----------------

If you opted not to use automated website provisioning use the following guidance.

Enable a Tomcat Instance
-----------------

The virtual machine comes with the common set of EBRC tomcat instances preinstalled and configured but they are in the disabled state so they do not unnecessarily consume system memory. Before installing a website, you will need to enable one or more of the tomcat instances using `instance_manager`.

    sudo instance_manager enable AmoebaDB

You may need to increase the memory in the `Vagrantfile` to run more than one tomcat instance. See Vagrant documentation for instructions.

Likewise, shutdown and disable an instance you no longer need with `instance_manager`.

    sudo instance_manager disable AmoebaDB


Install a Website
-----------------

Once logged in to the VM as the `vagrant` user, run

    installWdkSite

and follow instructions. The hostname is preconfigured to be `webdev.vm.apidb.org` in the `Vagrantfile` so you can readily create a website with that hostname.

If are using the Landrush plugin, you can edit the `config.landrush.tld` array in `Vagrantfile` to include project vanity domains - allowing you, for example, to have websites for sa.vm.toxodb.org and sa.vm.amoebadb.org. See '**About Apache VirtualHost Names**' below for more details on hostname.

Website Maintenance
-------------------

The virtual machine uses the same environment as physical servers so standard operating procedures apply. See summary list of tools at https://wiki.apidb.org/index.php/WebsiteMaintenanceScripts

----

About Apache VirtualHost Names
------------------------------

The convention is to use `vm.*.org` subdomains of our project domains as hostnames. This allows us to have Landrush to configure the local DNS to handle any request to those subdomains (e.g. `sa.vm.toxodb.org`) and direct them to the guest virtual machine while allowing primary domain requests to pass through, so requests to `www.toxodb.org` are directed to our physical servers.

In short, for OS X hosts, I recommend using the Landrush plugin and using a vagrant configuration something like

    config.vm.hostname = 'sa.vm.toxodb.org'
    config.landrush.tld = 'vm.toxodb.org'

and installing your website with a matching hostname, e.g. `sa.vm.toxodb.org`. (The `sa` name is not important, you can choose any name you prefer).

With this setup, pointing your browser at http://sa.vm.toxodb.org/ will show you the virtual machine, http://toxodb.org/ will take you to the live production website.


Known Issues
------------

Put `$PROJECT_HOME` on an NFS share somehow so it can be edited with host IDE. (I manually make a `project_home` directory on `/vagrant/scratch` and symlink it in `/var/www/sa.vm.toxodb.org/`. There are many other options to explore.

Many other things to be discovered.
