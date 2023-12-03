class ForcedFailureError(Exception):
    def __init__(self):
        self.message = "Failure in order service!"
        super().__init__(self.message)
