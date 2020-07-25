import click

from myapp import app, db
from myapp.models import Nickname, Article

@app.cli.command()
@click.option('--drop', is_flag=True, help='creat after drop')
def initdb(drop):
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('重置資料庫')

@app.cli.command()
@click.option('--admin', prompt=True, help='used to login')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='used to login')
def create_admin(admin, password):
    db.create_all()

    admin_name = Nickname.query.first()
    if admin_name is not None:
        click.echo('updating...')
        admin_name.admin = admin
        admin_name.set_password(password)

    else:
        click.echo('creating admin...')
        admin_name = Nickname(admin=admin, name='houshanyun')
        admin_name.set_password(password)
        db.session.add(admin_name)

    db.session.commit()
    click.echo('Done')
    

    
