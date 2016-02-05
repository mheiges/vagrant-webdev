Vagrant.configure(2) do |config|

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
   config.landrush.tld = ['vm.apidb.org', 'vm.cryptodb.org', 'vm.toxodb.org']
   config.landrush.host 'sa.vm.toxodb.org', '192.168.100.100'
   config.landrush.host 'sa.vm.cryptodb.org', '192.168.100.100'
  end

#   config.vm.provision :ansible do |ansible|
#     ansible.playbook = "playbook.yml"
#   end

end
