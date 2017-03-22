**Experimental**, unsupported provisioning of WDK-based EBRC website.

    bin/installwdksite

    ansible-playbook \
      -i .vagrant/provisioners/ansible/inventory/vagrant_ansible_inventory \
      --private-key=.vagrant/machines/default/virtualbox/private_key\
      -u vagrant --ssh-common-args='-o IdentitiesOnly=yes' \
      --extra-vars "settings_file=$PWD/installsite.yml" \
      playbook.yml

The `playbook.yml` does a base installation and, optionally, builds and configures a EBRC website.

The `printsettings.yml` playbook prints fact values, useful for debugging.


## extra-vars

`settings_file` - (required) location of file with installation variables
that supplement and optionally override values from /dashboard. This is
where you define installation variables

#### A note about combining lists in settings

List items (e.g. svn) are not individually mergeable (combining lists is
a union operation) so if you want to use, say, /dashboard's svn location
but change the branch of only one of the `remote` values you will need
to set the full list of svn locations in the property file.

    svn:
      locations:
        - location:
            local: "install"
            remote: "https://www.cbil.upenn.edu/svn/gus/install/branches/api-build-31"
        - location:
            local: "FgpUtil"
            remote: "https://www.cbil.upenn.edu/svn/gus/FgpUtil/branches/api-build-31"
and so on.

## Tips

The property file is YAML format however JSON is a subset of YAML so you
can usually plop in JSON when it's convenient. For example, say you want
to use the same svn locations as another site except you want to change
the branch of one of the locations. As noted above, you have to define
the full svn location list in the property file to achieve this because
lists are unions not merges. You can get svn locations from a /dashboard
JSON API 
    curl -s http://q2.toxodb.org/dashboard/json | jq .svn.locations
and copy/paste the results into the property file, then
edit the branch you want to change. 


    svn:
      locations:
        [
          {
            "location": {
              "remote": "https://www.cbil.upenn.edu/svn/gus/install/trunk",
              "local": "install",
              "revision": "19867"
            }
          },
          {
            "location": {
              "remote": "https://www.cbil.upenn.edu/svn/gus/FgpUtil/branches/api-build-1",
              "local": "FgpUtil",
              "revision": "19867"
            }
          }
        ]

## TO DO

- change tomcat.webapp to tomcat.context in /dashboard
- add Tomcat version to /dashboard and use to derive major_version