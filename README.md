A Vagrant Demo For EBRC Website Development
===========================================

This is an very incomplete starter project for EBRC website development. Copy it, make it your own, commit it to your own repository.

It uses a Vagrant box that was hastily converted from the legacy KVM template used for standalone website VMs. So treat it as a proof of concept and chance to identify features needed in our next generation VM templates.

The provisioning will install a CrytpoDB and a ToxoDB tomcat instance and start them.


Setup
=====

Install Vagrant
---------------

https://www.vagrantup.com/downloads.htm

Install VirtualBox
------------------

https://www.virtualbox.org/wiki/Downloads

Install Ansible
---------------

http://docs.ansible.com/ansible/intro_installation.html

Install Ansible Supporting Roles
--------------------------------

Checkout `eupathdb-ansible-roles` on the host in a path of your choice. These roles are meant to be shared and reused across multiple environments so it's recommended that you put it in some central place.

    cd /Users/jdoe/Repositories/ansible-roles
    git clone https://github.com/EuPathDB/ansible-tomcat_instance.git tomcat_instance

Inform Ansible of these roles by setting the `roles_path` in `~/.ansible.cfg` (create file as needed) to your central roles directory.

    [defaults] 
    roles_path = /Users/jdoe/Repositories/ansible-roles

_To collaborate on role development, commit changes to your own [Github fork](https://help.github.com/articles/fork-a-repo/) of the repository and [submit pull requests](https://help.github.com/articles/using-pull-requests/)._

Install the Landrush Plugin (Optional)
--------------------------------------

The [Landrush](https://github.com/phinze/landrush) plugin for Vagrant provides a local DNS so you can register guest hostnames and refer to them in the host browser. It is not strictly required but it makes life easier than editing `/etc/hosts` files. This plugin has maximum benefit for OS X hosts, some benefit for Linux hosts and no benefit for Windows. Windows hosts will need to edit `hosts` files.

    vagrant plugin install landrush

_If you have trouble getting the host to resolve guest hostnames through landrush try clearing the host DNS cache by running_ `sudo killall -HUP mDNSResponder`.

If you want to host multiple product sites - say, sa.vm.toxodb.org and sa.vm.giardiadb.org - you may want our Landrush fork that supports multiple TLD management. Until and unless our Pull Request is accepted by the upstream maintainer you will have to manually build and install the plugin from source.

    git clone https://github.com/mheiges/landrush.git
    cd landrush
    rake build
    vagrant plugin install pkg/landrush-0.18.0.gem

Clone This Vagrant Project
--------------------------

    clone https://github.com/mheiges/vagrant-webdev-poc.git

Start the Virtual Machine
-------------------------

    cd vagrant-webdev-poc
    vagrant up


Install a Website
-----------------

Run

    installWdkSite

and follow instructions.

This example project only installs ToxoDB and CryptoDB tomcat instances. To install another, add a role to `playbook.yml`

    - { role: tomcat_instance, product: PlasmoDB }

or edit an existing and then run `vagrant provision`. The VM has a relatively low memory footprint so you probably don't want to install extraneous instances.

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

Things that need to be coded in the provisioning, or otherwise handled in next generation VMs, include

Install Oracle drivers to tomcat, e.g.

    sudo cp $ORACLE_HOME/jdbc/lib/ojdbc6.jar \
    /usr/local/tomcat_instances/ToxoDB/shared/lib/
    
    sudo instance_manager restart ToxoDB

Put `$PROJECT_HOME` on an NFS share somehow so it can be edited with host IDE. (I manually make a `project_home` directory on `/vagrant/scratch` and symlink it in `/var/www/sa.vm.toxodb.org/`. There are many other options to explore.


If you put your site on an NFS volume `rebuilder` will rightly complain you don't own the files. Remove the ownership check from the script and it will work fine. Here's a patch:

    --- /usr/local/bin/rebuilder.dist	2015-09-04 11:01:55.000000000 -0400
    +++ /usr/local/bin/rebuilder	2015-09-03 11:36:57.000000000 -0400
    @@ -591,15 +591,6 @@
         exit 1
     fi
 
    -for f in $SITE_SYMLINK/{,gus_home/{bin,data,doc,lib,test,wsf-lib},project_home,html,cgi-bin,cgi-lib,conf,webapp}; do 
    -    if [[ -e $f && ! -O $f ]]; then
    -        echo
    -        echo "'$f' is not owned by you. I refuse to continue."
    -        echo
    -        exit 1
    -    fi
    -done
    -
     if [[ -n "$USER_BUILDROOT" && ! -d "$PROJECT_HOME/$USER_BUILDROOT" ]]; then
         echo "<$this> Fatal: Invalid --buildroot value."
         echo "'$USER_BUILDROOT' does not exist in '$PROJECT_HOME'"

Disable website password requirement

See __Removing the login requirement from a website__ at https://wiki.apidb.org/index.php/QaAuth .

Many other things to be discovered.
