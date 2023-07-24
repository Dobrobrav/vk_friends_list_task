class InvalidInputError(Exception):
    arg_name: str
    expected_value_descr: str
    log_error_descr: str

    def __init__(self,
                 arg_name: str,
                 expected_value_descr: str,
                 log_error_descr: str,
                 ) -> None:
        self.arg_name = arg_name
        self.expected_value_descr = expected_value_descr
        self.log_error_descr = log_error_descr


class UnexpectedVkError(Exception):
    pass
