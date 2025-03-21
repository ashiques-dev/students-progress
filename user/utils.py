def check_is_user(user):
    if not user.is_authenticated or user.is_superuser:
        return False
    return True
