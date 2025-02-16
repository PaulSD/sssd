""" Automation of proxy provider suite

:requirement: IDM-SSSD-REQ : Proxy Provider
:casecomponent: sssd
:subsystemteam: sst_idm_sssd
:upstream: yes
"""
from __future__ import print_function
import subprocess
import time
import os
import pytest
import ldap
from pexpect import pxssh
from sssd.testlib.common.utils import sssdTools, LdapOperations
from sssd.testlib.common.libkrb5 import krb5srv


def execute_cmd(multihost, command):
    """ Execute command on client """
    cmd = multihost.client[0].run_command(command)
    return cmd


@pytest.fixture(scope='function')
def proxy_sleep(multihost, request):
    """ Create sssd proxy pam ldap config file """
    execute_cmd(multihost, "echo 'auth required pam_exec.so "
                           "/usr/bin/sleep 100' > "
                           "/etc/pam.d/proxy_sleep")
    execute_cmd(multihost, "echo 'password required pam_exec.so "
                           "/usr/bin/sleep 100' >> "
                           "/etc/pam.d/proxy_sleep")
    execute_cmd(multihost, "echo 'account required pam_exec.so "
                           "/usr/bin/sleep 100' >> "
                           "/etc/pam.d/proxy_sleep")
    execute_cmd(multihost, "echo 'session required pam_exec.so "
                           "/usr/bin/sleep 100' >> "
                           "/etc/pam.d/proxy_sleep")

    def removeproxyldap():
        """ Remove sssd proxy pam ldap config file """
        remote = '/etc/pam.d/proxy_sleep'
        cmd = 'rm -f %s' % remote
        multihost.client[0].run_command(cmd)
    request.addfinalizer(removeproxyldap)


@pytest.fixture(scope='class')
def create_user_with_cn(multihost, request):
    """
        Configure sssd.conf
        Create a dedicated user with
        a DN starting e.g. with cn=...
        Create a local user foo12
    """
    ldap_uri = 'ldap://%s' % multihost.master[0].sys_hostname
    ds_rootdn = 'cn=Directory Manager'
    ds_rootpw = 'Secret123'
    ldap_inst = LdapOperations(ldap_uri, ds_rootdn, ds_rootpw)
    krb = krb5srv(multihost.master[0], 'EXAMPLE.TEST')
    user_info = {'cn': 'foo12'.encode('utf-8'),
                 'sn': 'foo12'.encode('utf-8'),
                 'uid': 'foo12'.encode('utf-8'),
                 'homeDirectory': '/home/foo12'.encode('utf-8'),
                 'objectClass': [b'top',
                                 b'inetOrgPerson',
                                 b'organizationalPerson',
                                 b'person',
                                 b'posixAccount'],
                 'uidNumber': '1458310'.encode('utf-8'),
                 'gidNumber': '1456410'.encode('utf-8')}
    user_dn = 'cn=foo12,ou=People,dc=example,dc=test'
    (_, _) = ldap_inst.add_entry(user_info, user_dn)
    krb.add_principal('foo12', 'user', 'Secret123')
    execute_cmd(multihost, "useradd foo12")
    execute_cmd(multihost, "echo Secret123 | passwd --stdin foo12")
    client = multihost.client[0]
    file_location = '/script/sssdproxymisc.sh'
    client.transport.put_file(os.path.dirname(os.path.abspath(__file__))
                              + file_location,
                              '/tmp/sssdproxymisc.sh')
    execute_cmd(multihost, "chmod 755 /tmp/sssdproxymisc.sh")

    def restoresssdconf():
        """ Restore sssd.conf """
        execute_cmd(multihost, "userdel -rf foo12")
        ldap_inst.del_dn('cn=foo12,ou=People,dc=example,dc=test')
        krb.delete_principal('foo12')
        execute_cmd(multihost, "rm -vf /tmp/sssdproxymisc.sh")

    request.addfinalizer(restoresssdconf)


@pytest.mark.usefixtures('setup_sssd_krb',
                         'create_posix_usersgroups',
                         'sssdproxyldap',
                         'install_nslcd',
                         'create_user_with_cn',
                         'netgroups')
@pytest.mark.tier1_3
class TestProxyMisc(object):
    """
    This is test case class for proxy provider suite
    """
    @staticmethod
    def test_bz1036758(multihost, backupsssdconf):
        """
        :title: Allow for custom attributes in RDN bz1036758
        :bugzilla: https://bugzilla.redhat.com/show_bug.cgi?id=1036758
        :id: 10eb49a4-b252-11ec-87ea-845cf3eff344
        :steps:
          1. sssd to fetch id information from local user
          2. Auth should work using ldap provider
        :expectedresults:
          1. Should succeed
          2. Should succeed
        """
        tools = sssdTools(multihost.client[0])
        domain_name = tools.get_domain_section_name()
        domain_params = {'id_provider': 'proxy',
                         'proxy_lib_name': 'files',
                         'auth_provider': 'ldap'}
        tools.sssd_conf('domain/' + domain_name, domain_params)
        tools.clear_sssd_cache()
        # Auth should work using ldap provider
        execute_cmd(multihost, "chown -R foo12 ~foo12")
        execute_cmd(multihost, "chown -R foo12 /var/spool/mail/foo12")
        # error logged in log
        execute_cmd(multihost, "systemctl stop sssd.service")
        execute_cmd(multihost, "rm -rf /var/lib/sss/{db,mc}/*")
        execute_cmd(multihost, "systemctl start sssd.service")

    @staticmethod
    def test_bz785902(multihost):
        """
        :title: Errors with empty loginShell and proxy provider bz785902
        :bugzilla: https://bugzilla.redhat.com/show_bug.cgi?id=785902
        :id: 17831b7a-b252-11ec-9942-845cf3eff344
        :steps:
          1. Adding the user in ldap server with empty login shell
          2. Search for Internal Error
          3. Non existing netgroup returned with proxy
             provider when proxy lib name is ldap
        :expectedresults:
          1. Should succeed
          2. Should not succeed
          3. Should not succeed
        """
        # Errors with empty loginShell and proxy provider bz785902
        tools = sssdTools(multihost.client[0])
        master_e = multihost.master[0].ip
        ldap_uri = f'ldap://{master_e}'
        ds_rootdn = 'cn=Directory Manager'
        ds_rootpw = 'Secret123'
        ldap_inst = LdapOperations(ldap_uri, ds_rootdn, ds_rootpw)
        user_dn = 'uid=foo1,ou=People,dc=example,dc=test'
        del_member = [(ldap.MOD_REPLACE, 'loginShell', "".encode('utf-8'))]
        (ret, _) = ldap_inst.modify_ldap(user_dn, del_member)
        assert ret == 'Success'
        domain_name = tools.get_domain_section_name()
        domain_params = {'use_fully_qualified_names': 'False',
                         'id_provider': 'proxy',
                         'auth_provider': 'proxy',
                         'cache_credentials': 'true',
                         'proxy_lib_name': 'ldap',
                         'proxy_pam_target': 'sssdproxyldap'}
        tools.sssd_conf('domain/' + domain_name, domain_params)
        tools.clear_sssd_cache()
        execute_cmd(multihost, "id foo1")
        del_member = [(ldap.MOD_REPLACE, 'loginShell',
                       "/bin/bash".encode('utf-8'))]
        (ret, _) = ldap_inst.modify_ldap(user_dn, del_member)
        assert ret == 'Success'
        for error_error in ['[sysdb_set_entry_attr] (6): '
                            'Error: 14 (Bad address)',
                            '[sysdb_store_user] (6): '
                            'Error: 14 (Bad address)',
                            'Internal Error (Cannot make/remove '
                            'an entry for the specified session)']:
            with pytest.raises(subprocess.CalledProcessError):
                execute_cmd(multihost, f"grep {error_error} /var/log/sssd/*")

    @staticmethod
    def test_bz804103(multihost):
        """
        :title: Nss-pam-ldapd returns empty netgroup when a
         nonexistent netgroup is requested
        :bugzilla: https://bugzilla.redhat.com/show_bug.cgi?id=804103
        :id: 9b2b7be0-ca01-11ec-9be1-845cf3eff344
        :steps:
            1. Check non existing netgroup
            2. Clear cache
            3. Check existing netgroup
            4. Again check non existing netgroup
        :expectedresults:
            1. Should not Succeed
            2. Should Succeed
            3. Should Succeed
            4. Should not Succeed
        """
        # non existing netgroup returned with proxy provider
        # when proxy lib name is ldap bz804103
        tools = sssdTools(multihost.client[0])
        with pytest.raises(subprocess.CalledProcessError):
            execute_cmd(multihost, "getent netgroup testsumgroup")
        tools.clear_sssd_cache()
        execute_cmd(multihost, "getent netgroup netgroup_1")
        with pytest.raises(subprocess.CalledProcessError):
            execute_cmd(multihost, "getent netgroup testsumgroup")

    @staticmethod
    def test_bz801377(multihost, backupsssdconf):
        """
        :title: Non existing netgroup returned with proxy provider
         when proxy lib name is file bz801377
        :bugzilla: https://bugzilla.redhat.com/show_bug.cgi?id=801377
        :id: 6ec16a9a-ca03-11ec-9675-845cf3eff344
        :steps:
          1. Configure proxy lib name is file
          2. Check for non existing group
          3. Configure /etc/negoup file
          4. Check netgoup name from /etc/netgroup
        :expectedresults:
          1. Should succeed
          2. Should not Succeed
          3. Should Succeed
          4. Should Succeed
        """
        tools = sssdTools(multihost.client[0])
        domain_name = tools.get_domain_section_name()
        domain_params = {'use_fully_qualified_names': 'False',
                         'id_provider': 'proxy',
                         'auth_provider': 'proxy',
                         'cache_credentials': 'true',
                         'proxy_lib_name': 'files',
                         'proxy_pam_target': 'sssdproxyldap'}
        tools.sssd_conf('domain/' + domain_name, domain_params)
        tools.clear_sssd_cache()
        with pytest.raises(subprocess.CalledProcessError):
            execute_cmd(multihost, "getent netgroup testsumgroup")
        execute_cmd(multihost, "echo 'QAeng    "
                               "(host1.example.com, ami1, example.com)'"
                               " > /etc/netgroup")
        tools.clear_sssd_cache()
        execute_cmd(multihost, "getent netgroup QAeng")
        execute_cmd(multihost, 'echo "" > /etc/netgroup')

    @staticmethod
    def test_bz647816(multihost, backupsssdconf):
        """
        :title: More than 10 auth attempt times out bz647816
        :bugzilla: https://bugzilla.redhat.com/show_bug.cgi?id=647816
        :id: 201a44c0-b252-11ec-94b7-845cf3eff344
        :steps:
            1. Auth a user more than 12 times
            2. Search for Error
        :expectedresults:
            1. Should succeed
            2. Should not succeed
        """
        # more than 10 auth attempt times out bz647816
        tools = sssdTools(multihost.client[0])
        domain_name = tools.get_domain_section_name()
        domain_params = {'proxy_lib_name': 'ldap',
                         'debug_level': '0xFFF0'}
        tools.sssd_conf('domain/' + domain_name, domain_params)
        tools.clear_sssd_cache()
        for _ in range(12):
            tools.auth_from_client("foo1@example1", "Secret123")
        with pytest.raises(subprocess.CalledProcessError):
            execute_cmd(multihost, "grep 'All available child slots are full, "
                                   "queuing request' /var/log/sssd/*")

    @staticmethod
    def test_bz871424(multihost, backupsssdconf):
        """
        :title: authconfig chokes on sssd.conf with chpass_provider directive
        :bugzilla: https://bugzilla.redhat.com/show_bug.cgi?id=871424
        :id: ce5fe4d2-e6e0-11ec-af7d-845cf3eff344
        :steps:
            1. Configure SSSD chpass_provider = proxy
            2. Run authconfig --test
        :expectedresults:
            1. Should succeed
            2. Should succeed
        """
        # more than 10 auth attempt times out bz647816
        tools = sssdTools(multihost.client[0])
        domain_name = tools.get_domain_section_name()
        domain_params = {'id_provider': 'ldap',
                         'auth_provider': 'ldap',
                         'chpass_provider': 'proxy',
                         'proxy_pam_target': 'sssdproxyldap',
                         'ldap_schema': 'rfc2307',
                         'enumerate': 'false',
                         'cache_credentials': 'true'}
        tools.sssd_conf('domain/' + domain_name, domain_params)
        tools.clear_sssd_cache()
        execute_cmd(multihost, "authselect test sssd")

    @staticmethod
    def test_bz1221992(multihost, backupsssdconf):
        """
        :title: sssd_be segfault at 0 ip sp error 6 in libtevent.so.0.9.21
        :bugzilla: https://bugzilla.redhat.com/show_bug.cgi?id=1221992
        :id: a97bf86a-e6e3-11ec-a1ee-845cf3eff344
        :steps:
            1. Configure user=sssd in sssd.conf
            2. user should be able to change the
               password without segfault
        :expectedresults:
            1. Should succeed
            2. Should succeed
        """
        tools = sssdTools(multihost.client[0])
        domain_name = 'sssd'
        domain_params = {'user': 'sssd'}
        tools.sssd_conf(domain_name, domain_params)
        domain_name = tools.get_domain_section_name()
        domain_params = {'id_provider': 'ldap',
                         'auth_provider': 'ldap',
                         'chpass_provider': 'proxy',
                         'proxy_pam_target': 'sssdproxyldap',
                         'proxy_lib_name': 'ldap'}
        tools.sssd_conf('domain/' + domain_name, domain_params)
        execute_cmd(multihost, "> /var/log/messages")
        tools.clear_sssd_cache()
        execute_cmd(multihost, "sh /tmp/sssdproxymisc.sh")
        time.sleep(3)
        with pytest.raises(subprocess.CalledProcessError):
            execute_cmd(multihost, "grep 'segfault at 0 ip' /var/log/messages")
        assert 'sssd' in execute_cmd(multihost,
                                     "stat -c %G /var/lib/sss/pipes"
                                     "/private/sbus-dp_example1.*").stdout_text

    @staticmethod
    def test_0002_bz1209483(multihost, backupsssdconf):
        """
        :title: sssd does not work as expected when id provider
         equal to proxy and auth provider equal to ldap bz1209483
        :bugzilla: https://bugzilla.redhat.com/show_bug.cgi?id=1209483
        :id: 2fa4834c-b252-11ec-919d-845cf3eff344
        :steps:
          1. Add a local user with the same name as an existing ldap user
          2. set id provider equal to proxy and auth provider equal to ldap
          3. lookup local user
        :expectedresults:
          1. Should succeed
          2. Should succeed
          3. Should succeed
        """
        tools = sssdTools(multihost.client[0])
        # sssd does not work as expected when id provider equal to proxy
        # and auth provider equal to ldap bz1209483
        execute_cmd(multihost, "systemctl stop nslcd.service")
        execute_cmd(multihost, "systemctl stop sssd")
        ldap_s = multihost.master[0].run_command(
            "ldapsearch -x -LLL uid=foo2")
        assert "uid=foo2,ou=People,dc=example,dc=test" in ldap_s.stdout_text
        execute_cmd(multihost, "useradd -u 2001 foo2")
        execute_cmd(multihost,
                    "echo 'pam.d/         pam_ldap.conf' > /etc/pam")
        services = {'filter_groups': 'root', 'filter_users': 'root'}
        tools.sssd_conf('nss', services)
        domain_name = tools.get_domain_section_name()
        domain_params = {'debug_level': '0xFFF0',
                         'id_provider': 'proxy',
                         'proxy_lib_name': 'files',
                         'auth_provider': 'ldap',
                         'chpass_provider': 'ldap',
                         'cache_credentials': 'true',
                         'use_fully_qualified_names': 'False'}
        tools.sssd_conf('domain/' + domain_name, domain_params)
        tools.clear_sssd_cache()
        getent = execute_cmd(multihost, "getent passwd -s sss foo2")
        ssh_res = tools.auth_from_client("foo2", "Secret123") == 3
        execute_cmd(multihost, "userdel -rf foo2")
        assert "foo2:*:2001:2001::/home/foo2:/bin/bash" in getent.stdout_text
        assert ssh_res, "Ssh for user foo2 failed."

    @staticmethod
    def test_bz1368467(multihost, backupsssdconf, create_350_posix_users):
        """
        :title: sssd runs out of available child slots and
         starts queuing requests in proxy mode bz1368467
        :bugzilla: https://bugzilla.redhat.com/show_bug.cgi?id=1368467
        :id: 452376f2-e2f3-11ec-96b9-845cf3eff344
        :steps:
            1. Configure sssd with proxy
            2. Create 350 users
            3. Try to ssh with 350 users
            4. Logs should not have error 'All available
               child slots are full'
        :expectedresults:
            1. Should succeed
            2. Should succeed
            3. Should succeed
            4. Should succeed
        """
        tools = sssdTools(multihost.client[0])
        domain_name = tools.get_domain_section_name()
        domain_params = {'debug_level': '0xFFF0',
                         'id_provider': 'ldap',
                         'proxy_lib_name': 'ldap',
                         'proxy_pam_target': 'sssdproxyldap',
                         'auth_provider': 'proxy',
                         'chpass_provider': 'ldap',
                         'proxy_max_children': '10',
                         'use_fully_qualified_names': 'False'}
        tools.sssd_conf('domain/' + domain_name, domain_params)
        tools.clear_sssd_cache()
        # sssd runs out of available child slots and starts
        # queuing requests in proxy mode
        execute_cmd(multihost, "systemctl start nslcd.service")
        for i in range(1, 351):
            p_ssh = pxssh.pxssh(
                options={"StrictHostKeyChecking": "no",
                         "UserKnownHostsFile": "/dev/null"}
            )
            p_ssh.force_password = True
            try:
                p_ssh.login(multihost.client[0].ip, f"doo{i}", "Secret123")
                p_ssh.logout()
            except pxssh.ExceptionPxssh:
                # We just trigger condition and check logs
                pass
        with pytest.raises(subprocess.CalledProcessError):
            execute_cmd(multihost, "grep 'All available child slots are full, "
                                   "queuing request' /var/log/sssd/*")

    @staticmethod
    def test_bz1927195(multihost, backupsssdconf, proxy_sleep):
        """
        :title: sssd runs out of proxy child slots and
          doesn't clear the counter for Active requests
        :bugzilla: https://bugzilla.redhat.com/show_bug.cgi?id=1927195
        :id: 4c5b53e2-ec88-11ec-a41a-845cf3eff344
        :customerscenario: true
        :steps:
            1. Configure sssd with proxy
            2. Try sssctl user-checks user@domain 11 times
            3. Logs should have one error 'All available
               child slots are full'
            4. 11th user-check should cause error "" in logs
            5. 12th user-check should not cause error message in logs
        :expectedresults:
            1. Should succeed
            2. Should succeed
            3. Should succeed
            4. Logs should have single count of error
               message caused by 11th user-check
            5. Logs should have single count of error
               message from 11th user-check, as 12th user-check works
        """
        # When using authentication provider as proxy,
        # User authentication suddenly stops working and
        # starts working again only after restarting the sssd service.
        tools = sssdTools(multihost.client[0])
        domain_name = tools.get_domain_section_name()
        domain_params = {'debug_level': '9',
                         'id_provider': 'ldap',
                         'proxy_pam_target': 'proxy_sleep',
                         'auth_provider': 'proxy',
                         'chpass_provider': 'ldap',
                         'proxy_max_children': '10',
                         'enumerate': 'false',
                         'entry_cache_timeout': '300',
                         'access_provider': 'proxy'}
        tools.sssd_conf('domain/' + domain_name, domain_params)
        tools.clear_sssd_cache()
        sssctl_user_check = 'for i in {1..11}; do sssctl user-checks' \
                            ' foo1@example1 > /dev/null 2>&1 & done'
        execute_cmd(multihost, sssctl_user_check)
        time.sleep(3)
        result = execute_cmd(multihost, "grep -c 'All available "
                                        "child slots are full, "
                                        "queuing request' "
                                        "/var/log/sssd/sssd_example1.log")
        assert result.stdout_text == '1\n'
        time.sleep(60)
        sssctl_user_check = 'sssctl user-checks foo1@example1 ' \
                            '> /dev/null 2>&1 &'
        execute_cmd(multihost, sssctl_user_check)
        time.sleep(2)
        result = execute_cmd(multihost, "grep -c 'All available "
                                        "child slots are full, "
                                        "queuing request' "
                                        "/var/log/sssd/sssd_example1.log")
        assert result.stdout_text == '1\n'
