class ValidationException(Exception):
    def __init__(self, error_type, field, attempted_value, message="Validation failed"):
        super().__init__(message)
        self.error_type = error_type
        self.field = field
        self.attempted_value = attempted_value

class StakeValidationException(ValidationException):
    pass

class BetValidationException(ValidationException):
    pass

class LimitValidationException(ValidationException):
    pass

class ProbabilityValidationException(ValidationException):
    pass
