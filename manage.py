#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Django's command-line utility for administrative tasks."""

import os
import shutil
import sys
import datetime


def __ensure_db_migration_folders_exist():
    """Ensure that init files exist in the data dir for the migration files."""
    init_files = [
        "data/__init__.py",
        "data/db_migrations/__init__.py",
        "data/db_migrations/general/__init__.py",
        "data/db_migrations/competition/__init__.py",
        "data/db_migrations/django_celery_beat/__init__.py",
        "data/db_migrations/django_celery_beat_periodictask/__init__.py",
        "data/db_migrations/sessions/__init__.py",
        "data/db_migrations/auth/__init__.py",
        "data/db_migrations/authtoken/__init__.py",
        "data/db_migrations/admin/__init__.py",
        "data/db_migrations/contenttypes/__init__.py",
    ]

    if all([os.path.isfile(i) for i in init_files]) is False:
        for i in init_files:
            dir_only = "/".join(i.split("/")[:-1])
            os.makedirs(dir_only, exist_ok=True)
            open(i, "a").close()


def __copy_over_static_files():
    """copy image files in data folter to productionfiles"""
    only_img_files = [
        f
        for f in os.listdir("./data")
        if os.path.isfile(os.path.join("./data", f)) and any([i in f.lower() for i in [".jpg", ".png", ".jpeg"]])
    ]
    try:
        for img in only_img_files:
            shutil.copyfile(os.path.join("./data", img), os.path.join("./productionfiles", img))
    except Exception as e:
        print('Image copy error to folder "productionfiles"', e)


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sweepstake.settings")

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    INITIAL_ARGV = sys.argv.copy()

    __ensure_db_migration_folders_exist()

    if os.environ.get("RUN_MAIN", "false") == "false":
        print("Django Server was started at: " f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}")

        # Make data model migrations
        sys.argv = [INITIAL_ARGV[0], "makemigrations"]
        main()

        # Apply data model migrations
        sys.argv = [INITIAL_ARGV[0], "migrate"]
        main()

        # Load EURO 2024 if empty data
        from competition.models import Tournament

        _added_data = False
        if len(Tournament.objects.all()) == 0:
            print("Add Email templates")
            sys.argv = [INITIAL_ARGV[0], "add_email_templates"]
            main()

            print("Add EURO 2024 data")
            sys.argv = [INITIAL_ARGV[0], "add_EURO_2024_data"]
            main()

            _added_data = True

        # Create Admin
        from general.models import CustomUser

        if len(CustomUser.objects.filter(is_staff=True)) == 0:
            print('Create super user "admin"')
            CustomUser.objects.create_superuser(email="admin@admin.local", password="password")

        # Add Test users
        if _added_data and os.environ.get("ADD_TEST_DATA", "False").lower() == "true":
            print("Add test data")
            sys.argv = [INITIAL_ARGV[0], "add_test_data"]
            main()

    else:
        print(
            "Django auto-reloader process executes second instance of django. "
            "Please turn-off for production usage by executing: "
            '"python manage.py runserver --noreload"'
        )

    # Run server
    sys.argv = INITIAL_ARGV
    main()
