class ValidationResult:
    def __init__(self):
        self.success = True
        self.errors = []
        self.warnings = []

    def add_error(self, exception: Exception):
        self.success = False
        self.errors.append(str(exception))

    def add_warning(self, warning: str):
        self.warnings.append(warning)

    def report(self):
        return {
            "success": self.success,
            "errors": self.errors,
            "warnings": self.warnings
        }
