import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')

component_name = "strongswan"


def test_strongswan_is_installed(host):
    strongswan = host.package(component_name)
    assert strongswan.is_installed


def test_strongswan_files_exists(host):
    strongswan_files = [
        "/etc/strongswan/ipsec.secrets",
        "/etc/strongswan/ipsec.conf",
        "/etc/strongswan/ipsec.d/certs/server.crt",
        "/etc/strongswan/ipsec.d/private/server.key"
    ]
    for fl in strongswan_files:
        assert host.file(fl).exists


def test_kernel_parameters(host):
    assert host.sysctl("net.ipv4.conf.all.accept_redirects") == 0
    assert host.sysctl("net.ipv4.conf.all.send_redirects") == 0
    assert host.sysctl("net.ipv4.ip_forward") == 1


def test_strongswan_service_running(host):
    svc_name = host.service(component_name)
    assert svc_name.is_running
    assert svc_name.is_enabled
    assert host.socket("udp://0.0.0.0:500").is_listening
    assert host.socket("udp://0.0.0.0:4500").is_listening
