/*
    Generated by sbus code generator

    Copyright (C) 2017 Red Hat

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

#ifndef _SBUS_IFP_CLIENT_SYNC_H_
#define _SBUS_IFP_CLIENT_SYNC_H_

#include <errno.h>
#include <talloc.h>
#include <tevent.h>

#include "sbus/sbus_sync.h"
#include "responder/ifp/ifp_iface/sbus_ifp_client_properties.h"
#include "responder/ifp/ifp_iface/ifp_iface_types.h"

errno_t
sbus_call_ifp_FindBackendByName
    (TALLOC_CTX *mem_ctx,
     struct sbus_sync_connection *conn,
     const char *busname,
     const char *object_path,
     const char * arg_name,
     const char ** _arg_backend);

errno_t
sbus_call_ifp_FindDomainByName
    (TALLOC_CTX *mem_ctx,
     struct sbus_sync_connection *conn,
     const char *busname,
     const char *object_path,
     const char * arg_name,
     const char ** _arg_domain);

errno_t
sbus_call_ifp_FindMonitor
    (TALLOC_CTX *mem_ctx,
     struct sbus_sync_connection *conn,
     const char *busname,
     const char *object_path,
     const char ** _arg_monitor);

errno_t
sbus_call_ifp_FindResponderByName
    (TALLOC_CTX *mem_ctx,
     struct sbus_sync_connection *conn,
     const char *busname,
     const char *object_path,
     const char * arg_name,
     const char ** _arg_responder);

errno_t
sbus_call_ifp_GetUserAttr
    (TALLOC_CTX *mem_ctx,
     struct sbus_sync_connection *conn,
     const char *busname,
     const char *object_path,
     const char * arg_user,
     const char ** arg_attr,
     DBusMessage **_reply);

errno_t
sbus_call_ifp_GetUserGroups
    (TALLOC_CTX *mem_ctx,
     struct sbus_sync_connection *conn,
     const char *busname,
     const char *object_path,
     const char * arg_user,
     const char *** _arg_values);

errno_t
sbus_call_ifp_ListBackends
    (TALLOC_CTX *mem_ctx,
     struct sbus_sync_connection *conn,
     const char *busname,
     const char *object_path,
     const char *** _arg_backends);

errno_t
sbus_call_ifp_ListComponents
    (TALLOC_CTX *mem_ctx,
     struct sbus_sync_connection *conn,
     const char *busname,
     const char *object_path,
     const char *** _arg_components);

errno_t
sbus_call_ifp_ListDomains
    (TALLOC_CTX *mem_ctx,
     struct sbus_sync_connection *conn,
     const char *busname,
     const char *object_path,
     const char *** _arg_domain);

errno_t
sbus_call_ifp_ListResponders
    (TALLOC_CTX *mem_ctx,
     struct sbus_sync_connection *conn,
     const char *busname,
     const char *object_path,
     const char *** _arg_responders);

errno_t
sbus_call_ifp_Ping
    (TALLOC_CTX *mem_ctx,
     struct sbus_sync_connection *conn,
     const char *busname,
     const char *object_path,
     const char * arg_ping,
     const char ** _arg_pong);

errno_t
sbus_call_ifp_cache_List
    (TALLOC_CTX *mem_ctx,
     struct sbus_sync_connection *conn,
     const char *busname,
     const char *object_path,
     const char *** _arg_result);

errno_t
sbus_call_ifp_cache_ListByDomain
    (TALLOC_CTX *mem_ctx,
     struct sbus_sync_connection *conn,
     const char *busname,
     const char *object_path,
     const char * arg_domain_name,
     const char *** _arg_result);

errno_t
sbus_call_ifp_cache_object_Remove
    (struct sbus_sync_connection *conn,
     const char *busname,
     const char *object_path,
     bool* _arg_result);

errno_t
sbus_call_ifp_cache_object_Store
    (struct sbus_sync_connection *conn,
     const char *busname,
     const char *object_path,
     bool* _arg_result);

errno_t
sbus_call_ifp_domain_ActiveServer
    (TALLOC_CTX *mem_ctx,
     struct sbus_sync_connection *conn,
     const char *busname,
     const char *object_path,
     const char * arg_service,
     const char ** _arg_server);

errno_t
sbus_call_ifp_domain_IsOnline
    (struct sbus_sync_connection *conn,
     const char *busname,
     const char *object_path,
     bool* _arg_status);

errno_t
sbus_call_ifp_domain_ListServers
    (TALLOC_CTX *mem_ctx,
     struct sbus_sync_connection *conn,
     const char *busname,
     const char *object_path,
     const char * arg_service_name,
     const char *** _arg_servers);

errno_t
sbus_call_ifp_domain_ListServices
    (TALLOC_CTX *mem_ctx,
     struct sbus_sync_connection *conn,
     const char *busname,
     const char *object_path,
     const char *** _arg_services);

errno_t
sbus_call_ifp_domain_RefreshAccessRules
    (struct sbus_sync_connection *conn,
     const char *busname,
     const char *object_path);

errno_t
sbus_call_ifp_groups_FindByID
    (TALLOC_CTX *mem_ctx,
     struct sbus_sync_connection *conn,
     const char *busname,
     const char *object_path,
     uint32_t arg_id,
     const char ** _arg_result);

errno_t
sbus_call_ifp_groups_FindByName
    (TALLOC_CTX *mem_ctx,
     struct sbus_sync_connection *conn,
     const char *busname,
     const char *object_path,
     const char * arg_name,
     const char ** _arg_result);

errno_t
sbus_call_ifp_groups_ListByDomainAndName
    (TALLOC_CTX *mem_ctx,
     struct sbus_sync_connection *conn,
     const char *busname,
     const char *object_path,
     const char * arg_domain_name,
     const char * arg_name_filter,
     uint32_t arg_limit,
     const char *** _arg_result);

errno_t
sbus_call_ifp_groups_ListByName
    (TALLOC_CTX *mem_ctx,
     struct sbus_sync_connection *conn,
     const char *busname,
     const char *object_path,
     const char * arg_name_filter,
     uint32_t arg_limit,
     const char *** _arg_result);

errno_t
sbus_call_ifp_group_UpdateMemberList
    (struct sbus_sync_connection *conn,
     const char *busname,
     const char *object_path);

errno_t
sbus_call_ifp_users_FindByCertificate
    (TALLOC_CTX *mem_ctx,
     struct sbus_sync_connection *conn,
     const char *busname,
     const char *object_path,
     const char * arg_pem_cert,
     const char ** _arg_result);

errno_t
sbus_call_ifp_users_FindByID
    (TALLOC_CTX *mem_ctx,
     struct sbus_sync_connection *conn,
     const char *busname,
     const char *object_path,
     uint32_t arg_id,
     const char ** _arg_result);

errno_t
sbus_call_ifp_users_FindByName
    (TALLOC_CTX *mem_ctx,
     struct sbus_sync_connection *conn,
     const char *busname,
     const char *object_path,
     const char * arg_name,
     const char ** _arg_result);

errno_t
sbus_call_ifp_users_FindByNameAndCertificate
    (TALLOC_CTX *mem_ctx,
     struct sbus_sync_connection *conn,
     const char *busname,
     const char *object_path,
     const char * arg_name,
     const char * arg_pem_cert,
     const char ** _arg_result);

errno_t
sbus_call_ifp_users_FindByValidCertificate
    (TALLOC_CTX *mem_ctx,
     struct sbus_sync_connection *conn,
     const char *busname,
     const char *object_path,
     const char * arg_pem_cert,
     const char ** _arg_result);

errno_t
sbus_call_ifp_users_ListByCertificate
    (TALLOC_CTX *mem_ctx,
     struct sbus_sync_connection *conn,
     const char *busname,
     const char *object_path,
     const char * arg_pem_cert,
     uint32_t arg_limit,
     const char *** _arg_result);

errno_t
sbus_call_ifp_users_ListByDomainAndName
    (TALLOC_CTX *mem_ctx,
     struct sbus_sync_connection *conn,
     const char *busname,
     const char *object_path,
     const char * arg_domain_name,
     const char * arg_name_filter,
     uint32_t arg_limit,
     const char *** _arg_result);

errno_t
sbus_call_ifp_users_ListByName
    (TALLOC_CTX *mem_ctx,
     struct sbus_sync_connection *conn,
     const char *busname,
     const char *object_path,
     const char * arg_name_filter,
     uint32_t arg_limit,
     const char *** _arg_result);

errno_t
sbus_call_ifp_user_UpdateGroupsList
    (struct sbus_sync_connection *conn,
     const char *busname,
     const char *object_path);

errno_t
sbus_get_ifp_components_debug_level
    (struct sbus_sync_connection *conn,
     const char *busname,
     const char *object_path,
     uint32_t* _value);

errno_t
sbus_get_ifp_components_enabled
    (struct sbus_sync_connection *conn,
     const char *busname,
     const char *object_path,
     bool* _value);

errno_t
sbus_get_ifp_components_name
    (TALLOC_CTX *mem_ctx,
     struct sbus_sync_connection *conn,
     const char *busname,
     const char *object_path,
     const char ** _value);

errno_t
sbus_get_ifp_components_providers
    (TALLOC_CTX *mem_ctx,
     struct sbus_sync_connection *conn,
     const char *busname,
     const char *object_path,
     const char *** _value);

errno_t
sbus_get_ifp_components_type
    (TALLOC_CTX *mem_ctx,
     struct sbus_sync_connection *conn,
     const char *busname,
     const char *object_path,
     const char ** _value);

errno_t
sbus_get_ifp_domains_backup_servers
    (TALLOC_CTX *mem_ctx,
     struct sbus_sync_connection *conn,
     const char *busname,
     const char *object_path,
     const char *** _value);

errno_t
sbus_get_ifp_domains_enumerable
    (struct sbus_sync_connection *conn,
     const char *busname,
     const char *object_path,
     bool* _value);

errno_t
sbus_get_ifp_domains_forest
    (TALLOC_CTX *mem_ctx,
     struct sbus_sync_connection *conn,
     const char *busname,
     const char *object_path,
     const char ** _value);

errno_t
sbus_get_ifp_domains_fully_qualified_name_format
    (TALLOC_CTX *mem_ctx,
     struct sbus_sync_connection *conn,
     const char *busname,
     const char *object_path,
     const char ** _value);

errno_t
sbus_get_ifp_domains_login_format
    (TALLOC_CTX *mem_ctx,
     struct sbus_sync_connection *conn,
     const char *busname,
     const char *object_path,
     const char ** _value);

errno_t
sbus_get_ifp_domains_max_id
    (struct sbus_sync_connection *conn,
     const char *busname,
     const char *object_path,
     uint32_t* _value);

errno_t
sbus_get_ifp_domains_min_id
    (struct sbus_sync_connection *conn,
     const char *busname,
     const char *object_path,
     uint32_t* _value);

errno_t
sbus_get_ifp_domains_name
    (TALLOC_CTX *mem_ctx,
     struct sbus_sync_connection *conn,
     const char *busname,
     const char *object_path,
     const char ** _value);

errno_t
sbus_get_ifp_domains_parent_domain
    (TALLOC_CTX *mem_ctx,
     struct sbus_sync_connection *conn,
     const char *busname,
     const char *object_path,
     const char ** _value);

errno_t
sbus_get_ifp_domains_primary_servers
    (TALLOC_CTX *mem_ctx,
     struct sbus_sync_connection *conn,
     const char *busname,
     const char *object_path,
     const char *** _value);

errno_t
sbus_get_ifp_domains_provider
    (TALLOC_CTX *mem_ctx,
     struct sbus_sync_connection *conn,
     const char *busname,
     const char *object_path,
     const char ** _value);

errno_t
sbus_get_ifp_domains_realm
    (TALLOC_CTX *mem_ctx,
     struct sbus_sync_connection *conn,
     const char *busname,
     const char *object_path,
     const char ** _value);

errno_t
sbus_get_ifp_domains_subdomain
    (struct sbus_sync_connection *conn,
     const char *busname,
     const char *object_path,
     bool* _value);

errno_t
sbus_get_ifp_domains_use_fully_qualified_names
    (struct sbus_sync_connection *conn,
     const char *busname,
     const char *object_path,
     bool* _value);

errno_t
sbus_get_ifp_group_gidNumber
    (struct sbus_sync_connection *conn,
     const char *busname,
     const char *object_path,
     uint32_t* _value);

errno_t
sbus_get_ifp_group_groups
    (TALLOC_CTX *mem_ctx,
     struct sbus_sync_connection *conn,
     const char *busname,
     const char *object_path,
     const char *** _value);

errno_t
sbus_get_ifp_group_name
    (TALLOC_CTX *mem_ctx,
     struct sbus_sync_connection *conn,
     const char *busname,
     const char *object_path,
     const char ** _value);

errno_t
sbus_get_ifp_group_uniqueID
    (TALLOC_CTX *mem_ctx,
     struct sbus_sync_connection *conn,
     const char *busname,
     const char *object_path,
     const char ** _value);

errno_t
sbus_get_ifp_group_users
    (TALLOC_CTX *mem_ctx,
     struct sbus_sync_connection *conn,
     const char *busname,
     const char *object_path,
     const char *** _value);

errno_t
sbus_get_ifp_user_domain
    (TALLOC_CTX *mem_ctx,
     struct sbus_sync_connection *conn,
     const char *busname,
     const char *object_path,
     const char ** _value);

errno_t
sbus_get_ifp_user_domainname
    (TALLOC_CTX *mem_ctx,
     struct sbus_sync_connection *conn,
     const char *busname,
     const char *object_path,
     const char ** _value);

errno_t
sbus_get_ifp_user_extraAttributes
    (TALLOC_CTX *mem_ctx,
     struct sbus_sync_connection *conn,
     const char *busname,
     const char *object_path,
     hash_table_t ** _value);

errno_t
sbus_get_ifp_user_gecos
    (TALLOC_CTX *mem_ctx,
     struct sbus_sync_connection *conn,
     const char *busname,
     const char *object_path,
     const char ** _value);

errno_t
sbus_get_ifp_user_gidNumber
    (struct sbus_sync_connection *conn,
     const char *busname,
     const char *object_path,
     uint32_t* _value);

errno_t
sbus_get_ifp_user_groups
    (TALLOC_CTX *mem_ctx,
     struct sbus_sync_connection *conn,
     const char *busname,
     const char *object_path,
     const char *** _value);

errno_t
sbus_get_ifp_user_homeDirectory
    (TALLOC_CTX *mem_ctx,
     struct sbus_sync_connection *conn,
     const char *busname,
     const char *object_path,
     const char ** _value);

errno_t
sbus_get_ifp_user_loginShell
    (TALLOC_CTX *mem_ctx,
     struct sbus_sync_connection *conn,
     const char *busname,
     const char *object_path,
     const char ** _value);

errno_t
sbus_get_ifp_user_name
    (TALLOC_CTX *mem_ctx,
     struct sbus_sync_connection *conn,
     const char *busname,
     const char *object_path,
     const char ** _value);

errno_t
sbus_get_ifp_user_uidNumber
    (struct sbus_sync_connection *conn,
     const char *busname,
     const char *object_path,
     uint32_t* _value);

errno_t
sbus_get_ifp_user_uniqueID
    (TALLOC_CTX *mem_ctx,
     struct sbus_sync_connection *conn,
     const char *busname,
     const char *object_path,
     const char ** _value);

errno_t
sbus_getall_ifp_components
    (TALLOC_CTX *mem_ctx,
     struct sbus_sync_connection *conn,
     const char *busname,
     const char *object_path,
     struct sbus_all_ifp_components **_properties);

errno_t
sbus_getall_ifp_domains
    (TALLOC_CTX *mem_ctx,
     struct sbus_sync_connection *conn,
     const char *busname,
     const char *object_path,
     struct sbus_all_ifp_domains **_properties);

errno_t
sbus_getall_ifp_group
    (TALLOC_CTX *mem_ctx,
     struct sbus_sync_connection *conn,
     const char *busname,
     const char *object_path,
     struct sbus_all_ifp_group **_properties);

errno_t
sbus_getall_ifp_user
    (TALLOC_CTX *mem_ctx,
     struct sbus_sync_connection *conn,
     const char *busname,
     const char *object_path,
     struct sbus_all_ifp_user **_properties);

#endif /* _SBUS_IFP_CLIENT_SYNC_H_ */
