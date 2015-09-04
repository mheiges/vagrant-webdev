A Vagrant Demo For EBRC Website Development
===========================================

This is an incomplete starter project for EBRC website development. Copy it, make it your own, commit it to your own repository.

Setup
=====

Install Vagrant
---------------


Install VirtualBox
------------------


Install Ansible
---------------


Install Ansible Supporting Roles
--------------------------------


Checkout `eupathdb-ansible-roles` on the host in a path of your choice. These roles are meant to be shared and reused across multiple environments.

    git clone https://github.com/EuPathDB/eupathdb-tomcat_instance tomcat_instance

Inform Ansible of these roles by setting the `roles_path` in `~/.ansible.cfg` (create file as needed) to your svn working directory.

    [defaults] 
    roles_path = /Users/jdoe/Repositories/ansible-roles

_To collaborate on role development, commit changes to your own [Github fork](https://help.github.com/articles/fork-a-repo/) of the repository and [submit pull requests](https://help.github.com/articles/using-pull-requests/)._

Install the Landrush Plugin (Optional)
--------------------------------------

The [Landrush](https://github.com/phinze/landrush) plugin for Vagrant provides a local DNS so you can register guest hostnames and refer to them in the host browser. It is not strictly required but it makes life easier than editing `/etc/hosts` files. This plugin has maximum benefit for OS X hosts, some benefit for Linux hosts and no benefit for Windows. Windows hosts will need to edit `hosts` files.

    vagrant plugin install landrush

_If you have trouble getting the host to resolve guest hostnames through landrush try clearing the host DNS cache by running_ `sudo killall -HUP mDNSResponder`.

If you want to host multiple product sites - say, toxodb.org and giardiadb.org - you may want our Landrush fork that supports multiple TLD management. Until and unless our Pull Request is accepted by the upstream maintainer you will have to manually build and install the plugin from source.

    git clone https://github.com/mheiges/landrush.git
    cd landrush
    rake build
    vagrant plugin install pkg/landrush-0.18.0.gem


