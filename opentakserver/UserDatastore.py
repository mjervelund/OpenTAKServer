from flask_security import SQLAlchemyUserDatastore


class UserDatastore(SQLAlchemyUserDatastore):

    def find_user(self, case_insensitive: bool = False, **kwargs):
        """
        Always look up usernames case insensitively, the same way the login form does
        (SECURITY_USER_IDENTITY_ATTRIBUTES). Otherwise someone who logs in as "Bob" is
        then not found as "Bob" by everything that looks them up by the username they
        typed, like ATAK's certificate enrollment
        """
        if "username" in kwargs:
            case_insensitive = True
        return super().find_user(case_insensitive=case_insensitive, **kwargs)
