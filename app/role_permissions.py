from app.functions.dependencies import RoleChecker

allow_create_users = RoleChecker(['admin'])
allow_update_users = RoleChecker(['admin', 'moderator'])
allow_delete_users = RoleChecker(["admin"])
allow_view_users_list = RoleChecker(['admin', 'moderator'])

allow_create_drafts = RoleChecker(['client'])
allow_update_drafts = RoleChecker(['client'])
allow_delete_drafts = RoleChecker(["client", 'admin', 'moderator'])

allow_create_advertisements = RoleChecker(['client'])
allow_update_advertisements = RoleChecker(['client'])
allow_delete_advertisements = RoleChecker(["client", 'admin', 'moderator'])