A Vagrant Demo For EBRC Website Development
===========================================

This is an very incomplete starter project for EBRC website development. Copy it, make it your own, commit it to your own repository.

It uses a Vagrant box that was hastily converted from the legacy KVM template used for standalone website VMs. So treat it as a proof of concept and chance to identify features needed in our next generation VM templates.

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

Apache VirtualHost Names
------------------------

The convention is to use `vm.*.org` subdomains of our project domains as hostnames. This allows us to have Landrush to configure the local DNS to handle any request to those subdomains (e.g. `sa.vm.toxodb.org`) and direct them to the guest virtual machine while allowing primary domain requests to pass through, so requests to `www.toxodb.org` are directed to our physical servers.

In short, for OS X hosts, I recommend using the Landrush plugin and using a vagrant configuration something like

    config.vm.hostname = 'sa.vm.toxodb.org'
    config.landrush.tld = 'vm.toxodb.org'

and installing your website with a matching hostname, e.g. `sa.vm.toxodb.org`. (The `sa` name is not important, you can choose any name you prefer).

With this setup, pointing your browser at http://sa.vm.toxodb.org/ will show you the virtual machine, http://toxodb.org/ will take you to the live production website.

