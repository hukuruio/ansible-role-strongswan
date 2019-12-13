import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')


def test_strongswan_is_installed(host):
    strongswan = host.package('strongswan')
    assert strongswan.is_installed
