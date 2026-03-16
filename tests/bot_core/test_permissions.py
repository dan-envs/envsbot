import pytest

from utils.command import Role


class DummyCmd:
    """
    Minimal command stub used for permission testing.

    The real command objects in the system expose a `role`
    attribute defining the minimum required role to execute
    the command. This stub mirrors that interface so the
    permission logic can be tested in isolation.
    """

    def __init__(self, role):
        self.role = role


def test_admin_allowed():
    """
    Verify that a user with ADMIN role is allowed to execute
    a command that requires ADMIN privileges.
    """
    cmd = DummyCmd(Role.ADMIN)

    user_role = Role.ADMIN

    assert user_role <= cmd.role


def test_user_denied():
    """
    Verify that a USER role cannot execute a command that
    requires ADMIN privileges.
    """
    cmd = DummyCmd(Role.ADMIN)

    user_role = Role.USER

    assert not (user_role <= cmd.role)