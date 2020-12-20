class EnvironmentException(EnvironmentError):
    """
    Exception type for handling invalid environment configuration.
    """
    def __init__(self, arg):
        self.strerror = arg
        self.args = {arg}


class MonitorException(ValueError):
    """
    Exception type for handling run-time monitoring.

    May be further sub-typed per model for log/alerting clarity.
    """
    def __init__(self, arg):
        self.strerror = arg
        self.args = {arg}
