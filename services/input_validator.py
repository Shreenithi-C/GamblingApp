from exceptions.validation_exceptions import *
from utils.enums import ValidationErrorType
from models.validation_result import ValidationResult

class ValidationConfig:
    def __init__(self, min_stake=100, max_stake=100000, min_bet=1, max_bet=10000,
                 min_prob=0.0, max_prob=1.0, strict_mode=True, allow_zero_stake=False):
        self.min_stake = min_stake
        self.max_stake = max_stake
        self.min_bet = min_bet
        self.max_bet = max_bet
        self.min_prob = min_prob
        self.max_prob = max_prob
        self.strict_mode = strict_mode
        self.allow_zero_stake = allow_zero_stake

class InputValidator:
    def __init__(self, config: ValidationConfig):
        self.config = config

    def validate_initial_stake(self, stake):
        result = ValidationResult()
        try:
            if stake is None:
                raise StakeValidationException(ValidationErrorType.NULL_ERROR, "stake", stake, "Stake cannot be null")
            if not isinstance(stake, (int, float)):
                raise StakeValidationException(ValidationErrorType.NUMERIC_ERROR, "stake", stake, "Stake must be numeric")
            if stake < 0:
                raise StakeValidationException(ValidationErrorType.STAKE_ERROR, "stake", stake, "Stake cannot be negative")
            if not self.config.allow_zero_stake and stake == 0:
                raise StakeValidationException(ValidationErrorType.STAKE_ERROR, "stake", stake, "Zero stake not allowed")
            if stake < self.config.min_stake or stake > self.config.max_stake:
                raise StakeValidationException(ValidationErrorType.RANGE_ERROR, "stake", stake, "Stake out of range")
        except ValidationException as e:
            result.add_error(e)
        return result

    def validate_bet_amount(self, bet, current_stake):
        result = ValidationResult()
        try:
            if bet <= 0:
                raise BetValidationException(ValidationErrorType.BET_ERROR, "bet", bet, "Bet must be positive")
            if bet > current_stake:
                raise BetValidationException(ValidationErrorType.BET_ERROR, "bet", bet, "Bet exceeds current stake")
            if bet < self.config.min_bet or bet > self.config.max_bet:
                raise BetValidationException(ValidationErrorType.RANGE_ERROR, "bet", bet, "Bet out of range")
        except ValidationException as e:
            result.add_error(e)
        return result

    def validate_limits(self, lower, upper):
        result = ValidationResult()
        try:
            if lower < 0 or upper < 0:
                raise LimitValidationException(ValidationErrorType.LIMIT_ERROR, "limits", (lower, upper), "Limits cannot be negative")
            if upper <= lower:
                raise LimitValidationException(ValidationErrorType.LIMIT_ERROR, "limits", (lower, upper), "Upper limit must be greater than lower limit")
        except ValidationException as e:
            result.add_error(e)
        return result

    def validate_probability(self, prob):
        result = ValidationResult()
        try:
            if prob is None:
                raise ProbabilityValidationException(ValidationErrorType.NULL_ERROR, "probability", prob, "Probability cannot be null")
            if not isinstance(prob, (int, float)):
                raise ProbabilityValidationException(ValidationErrorType.NUMERIC_ERROR, "probability", prob, "Probability must be numeric")
            if prob < self.config.min_prob or prob > self.config.max_prob:
                raise ProbabilityValidationException(ValidationErrorType.PROBABILITY_ERROR, "probability", prob, "Probability must be between 0 and 1")
        except ValidationException as e:
            result.add_error(e)
        return result
