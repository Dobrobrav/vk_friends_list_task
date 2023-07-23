
class IncorrectInput(Exception):
    arg_name: str
    expected_value_descr: str

    def __init__(self,
                 arg_name: str,
                 expected_value_descr: str,
                 ) -> None:
        self.arg_name = arg_name
        self.expected_value_descr = expected_value_descr
