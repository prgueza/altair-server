class UnValidVolumeError(Exception):
    """
    UnValidVolumeError: This exception gets raised when the volume does not correspond to any valid glass measure.
    Services which raise this exception will return a 403 status code indicating the request was malformed
    """

    def __init__(self, message):
        self.__code = 403
        self.__message = message

    @property
    def message(self):
        return self.__message

    @property
    def code(self):
        return self.__code

    @property
    def error(self):
        return {'status': self.code, 'message': self.message}


class NotFoundException(Exception):
    """
    NotFoundException: This custom exception gets raised when there is not associated resource for the requested path.
    This happens when the beer with the specified ID doesn't exist or the ID is invalid. Services which raise this
    exception will return a 404 status code indicating the resource was not found
    """

    def __init__(self, message):
        self.__code = 404
        self.__message = message

    @property
    def message(self):
        return self.__message

    @property
    def code(self):
        return self.__code

    @property
    def error(self):
        return {'status': self.code, 'message': self.message}
