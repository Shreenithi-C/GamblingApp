from services.input_validator import InputValidator
class SafeInputHandler:
    def __init__(self, validator: InputValidator):
        self.validator = validator

    def get_validated_input(self, prompt, validation_func, *args):
        while True:
            try:
                value = float(input(prompt))
                result = validation_func(value, *args) if args else validation_func(value)
                if result.success:
                    return value
                else:
                    print("Errors:", result.errors)
            except ValueError:
                print("Invalid numeric input. Please try again.")
