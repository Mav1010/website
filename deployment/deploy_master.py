from decouple import config
from fabric2 import Connection
from invoke.exceptions import UnexpectedExit


SSH_USER_WEBSITE = 'Mydevil10@s2.mydevil.net'
GIT_MASTER_BRANCH_NAME = 'master'
DOMAIN = 'jd-ubezpieczenia.pl'


def deploy_production():
    # connect to the server over SSH
    c = Connection(SSH_USER_WEBSITE, connect_kwargs={"password": config('SHH_PASSWORD')})

    # activate the virtual environment
    with c.prefix('source ~/.virtualenvs/website/bin/activate'):
        # move to /app/ directory where the app lives and GIT is initiated
        with c.cd('domains/jd-ubezpieczenia.pl/public_python'):

            # check the current GIT branch name
            current_branch = c.run('git rev-parse --abbrev-ref HEAD')
            # if for some reason it's not master, switch to master branch
            if not current_branch.stdout.strip() == GIT_MASTER_BRANCH_NAME:
                c.run('git checkout {}'.format(GIT_MASTER_BRANCH_NAME))

            # stash changes if there are any
            c.run('git stash')

            # update the code from Github
            c.run('git pull --rebase')

            # install requirements
            c.run('pip install -r requirements.txt')

            # run the migrations
            c.run('python manage.py migrate --no-input')

            # collect static
            c.run('python manage.py collectstatic --no-input')

            # restart the server
            c.run('devil www restart {}'.format(DOMAIN))

            # run celery
            # try:
            #     c.run('celery -A kitmondo control shutdown')
            # except UnexpectedExit:
            #     pass
            # c.run('celery -A kitmondo worker --loglevel=info -f ~/log/celery.log')


if __name__ == "__main__":
    deploy_production()