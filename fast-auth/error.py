from fastapi.exceptions import HTTPException


class NoSuchUserException(Exception):
    def __init__(self, message="No Such User"):
        raise HTTPException(status_code=400, detail=message)


class WrongPasswordException(Exception):
    def __init__(self, message="Wrong Password"):
        raise HTTPException(status_code=400, detail=message)


class AlreadyExistUsernameException(Exception):
    def __init__(self, message="Already exist username"):
        raise HTTPException(status_code=403, detail=message)
