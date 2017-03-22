products = [
  'ApiDB',
  'AmoebaDB',
  'CryptoDB',
  'EuPathDB',
  'FungiDB',
  'GiardiaDB',
  'HostDB',
  'MicrosporidiaDB',
  'OrthoMCL',
  'PiroplasmaDB',
  'PlasmoDB',
  'SchistoDB',
  'ToxoDB',
  'TrichDB',
  'TriTrypDB',
]
vagrant_root = File.dirname(__FILE__)
Vagrant.configure(2) do |config|

  config.vm.box_url = 'http://software.apidb.org/vagrant/webdev.json'
  config.vm.box = "ebrc/webdev"

  config.ssh.forward_agent = true

  config.vm.hostname = 'webdev.vm.apidb.org'
  
  config.vm.network :private_network, type: :dhcp
  config.vm.synced_folder ".", "/vagrant", type: "nfs"

  if Vagrant.has_plugin?('landrush')
    config.landrush.enabled = true
    # Setting multiple TLD values requires my Landrush
    # fork at https://github.com/mheiges/landrush.git
    # (A pull request for the patch as been sent to the upstream landrush maintainer.)
    config.landrush.tld = products.map{ |tld| "vm.#{tld.downcase}.org" }
    config.landrush.tld.each do |tld|
      config.landrush.host "sa.#{tld}"
    end
  end

  if File.file?("#{vagrant_root}/installsite.yml")
    config.vm.provision :ansible do |ansible|
      ansible.playbook = 'ansible/installwdksite/playbook.yml'
      if ! File.file?("#{vagrant_root}/nogalaxy")
        ansible.galaxy_role_file = 'ansible/installwdksite/requirements.yml'
        ansible.galaxy_roles_path = 'ansible/installwdksite/roles'
      end
      ansible.extra_vars = {
        settings_file: "#{vagrant_root}/installsite.yml"
      }
    end
  end

end
