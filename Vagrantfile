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

#   config.vm.provision :ansible do |ansible|
#     ansible.playbook = "playbook.yml"
#   end

end
