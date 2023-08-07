from commands import crud


def check_username(username: str):
    repeat = True
    while repeat:
        user = crud.get_user_by_username(username=username)
        if user:
            print(f'error: User named "{username}" already exists.')
            print("Try again...")
            username = input('Input username: ')
            continue
        else:
            repeat = False
    return username


def check_email(email: str):
    repeat = True
    while repeat:
        user = crud.get_user_by_email(email=email)
        if user:
            print(f'error: Email "{email}" is already taken.')
            print("Try again...")
            email = input('Input email: ')
            continue
        else:
            repeat = False
    return email

