## Using an non-default Tomcat instance for a WDK website

The `rebuilder` script defaults to using file path naming conventions to derive
the Tomcat instance. For example, give the site `sa.vm.trichdb.org` installed
and symbolically linked in `/var/www`,

```
$ ls -l /var/www/sa.vm.trichdb.org
/var/www/sa.vm.trichdb.org -> TrichDB/trichdb.b36
```

`rebuilder` will default to deploying the `trichdb.b36` webapp to the
`TrichDB` Tomcat instance.

To use a different Tomcat instance, say `Tomcat8`, you will need to update
Apache's configuration so it proxies to the different Tomcat instance and
tell `rebuilder` to use that instance.

### Patch the Apache vhost configuration file

In the Apache vhost configuration file, `/etc/httpd/conf/enabled_sites/sa.vm.trichdb.org.conf` (or whatever yours is named), add:

```
  <Perl>
  @JkMount = (
     [ "/$VH::Webapp/*" => "Tomcat8" ],
     [ "/$VH::Webapp"   => "Tomcat8" ],
  );
  </Perl>
```

after the "Configurations specific to this virtual host” comment.

Reload the webserver

```
$ sudo systemctl reload httpd
```

On virtual machines, enable the Tomcat8 instance.

```
$ sudo instance_manager enable Tomcat8 
```

### Change the `rebuilder` command line arguments

Use rebuilder with the `--webapp` option to specify the `Tomcat8` instance.

```
$ rebuilder --webapp Tomcat8:trichdb.b36 sa.vm.trichdb.org 
```

Substitute `trichdb.b36` with the name of your webapp and `sa.vm.trichdb.org` with the hostname for your site.

### cattail

If you use `cattail` for log monitoring, you will need to tell it
to use the logs in the alternate Tomcat instance.

```
$ cattail -ct sa.vm.trichdb.org Tomcat8
```