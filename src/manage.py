import typer
from getpass import getpass

from settings import settings
from commands import crud, check


app = typer.Typer()


@app.command()
def hello():
    txt = input('Input name: ')
    print(f'Hello {txt}')


@app.command()
def create(role: str):
    if role in settings.role_list:
        username = check.check_username(input('Input username: '))
        email = check.check_email(input('Input email: '))
        password = getpass('Input password: ')
        crud.create_user(
            username=username,
            email=email,
            role=role,
            password=password
        )
        print(f'Created {role} {username}')
    else:
        role_list = f"{', '.join(settings.role_list)}"
        print("usage: create [ROLE] {" + f"{role_list}" + "}")
        print()
        print(f"typer: error: invalid choice: '{role}' (choose from {role_list})")


if __name__ == "__main__":
    app()
