# exceptions


# exception for required field being empty

class RequiredFieldEmptyError(Exception):
    """Raised when a required field is empty"""
    pass


# exception for item not having enough info
class LessInfoThanExpectedError(Exception):
    """Raised when a row doesn't have all fields complete"""
    pass


# exception for no data on item
class NoDataOnRowError(Exception):
    """Raised when a row is empty"""
    pass
