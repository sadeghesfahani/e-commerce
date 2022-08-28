import os
import django
from django.core.management import execute_from_command_line
from django.db.models import ForeignKey

from e_commerce.settings import LOCAL_APP
from os import listdir
from os.path import isfile, join
import copy
from time import sleep
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "e_commerce.settings")

django.setup()


class SmoothRun:
    def __init__(self, problem, deploy=False, root="/usr/src/app"):
        if deploy:
            root = "/usr/src/app"
        self.root = root
        self.problem = False
        self.deploy = deploy
        self.is_migrate_working()
        if problem:
            print("\n\n =====>  smooth run started:")
            self.apps = list()
            self.get_local_apps()
            print("\n\n =====>  checking for issues")
            if self.is_make_migrations_working():
                self.is_migrate_working()
                print("\n\n =====>  no issue has been found")
            else:
                self.problem = True

                try:
                    print("\n\n =====>  server faced problem, we are trying to fix it automatically. getting backup")
                    os.system(f"cd {self.root} && python3 manage.py dumpdata > backup.json")
                except:
                    os.system(f"cd {self.root} && python3 manage.py dumpdata store > backup.json")

                print("\n\n =====>  makemigrations failed, deleting migration files")
                self.delete_migration_files(root)
                print("\n\n =====>  trying makemigrations")
                self.is_make_migrations_working()
                print("\n\n =====>  trying to migrate")
                if not self.is_migrate_working():
                    print("\n\n =====>  migration failed, trying to flush database")
                    self.make_zero()
        else:
            self.is_make_migrations_working()
            self.is_migrate_working()

        if self.problem:
            print("\n\n =====>  server faced problem, we are trying to fix it automatically")
            os.system(f"cd {self.root} && python3 manage.py loaddata ./backup.json")
            try:
                os.remove("./backup.json")
            except:
                pass
        execute_from_command_line(["manage.py", "initadmin"])
        if not self.deploy:
            self.run_server()
        else:
            os.system("python3 -m gunicorn -w 4 -b 0.0.0.0:8000 e_commerce.wsgi:application")
            exit()

    def get_local_apps(self, name_index=1):
        for apps in LOCAL_APP:
            self.apps.append(apps)

    def is_make_migrations_working(self):
        try:
            execute_from_command_line(["manage.py", "makemigrations"])
            return True
        except:
            return False

    def delete_migration_files(self, base_root):
        for app in self.apps:
            path = join(base_root, app)
            path = join(path, "migrations")
            for file in listdir(path):
                if isfile(join(path, file)) and file != "__init__.py":
                    os.remove(join(path, file))

    def is_migrate_working(self):
        try:
            execute_from_command_line(["manage.py", "migrate"])
            return True
        except:
            return False

    def make_zero(self):

        failed = list()
        apps = copy.deepcopy(self.apps)

        for app in self.apps:
            print("\n=>app:", app)
            try:
                execute_from_command_line(["manage.py", "migrate", app, "zero"])
                apps.remove(app)
            except:
                failed.append(app)

        while len(apps) > 0:
            print("\n=>inside while:", apps)
            final_failed = copy.deepcopy(failed)
            for index in range(len(failed)):
                # try:
                sleep(2)
                print("wtf=>", final_failed, failed, failed[index])
                execute_from_command_line(["manage.py", "migrate", failed[index], "zero"])
                apps.remove(failed[index])
                final_failed.remove([index])
                # except Exception as e:
                #     print(e)
            failed = copy.deepcopy(final_failed)
        if not self.is_migrate_working():
            self.fake_migrate()

    def fake_migrate(self):
        try:
            execute_from_command_line(["manage.py", "migrate", "--fake-initial"])
        except:
            try:
                execute_from_command_line(["manage.py", "sqlflush"])
            except:
                try:
                    execute_from_command_line(["manage.py", "reset_schema"])
                except:
                    print("\n\n =====>  there is nothing smooth run can do for you!")
        execute_from_command_line(["manage.py", "migrate", "--fake-initial"])

    def run_server(self):
        if self.problem:
            execute_from_command_line(["manage.py", "loaddata", "backup.json"])
            print("\n\n\n\n ****Happy to save you time**** \n\n\n")

        # print("\n\n =====>  from here, there is nothing to do with database\n")

        # sina = execute_from_command_line(["django-admin", "dumpdata","store > backup.json" ])
        # print(sina)


        execute_from_command_line(["manage.py", "runserver", "0.0.0.0:8000"])


deploy = True if os.environ['DJANGO_DEBUG'] == "False" else False
print(deploy)
SmoothRun(True, deploy)
