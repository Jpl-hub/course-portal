import os
import sys


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "course_portal.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Django is required to run management commands. Install from requirements.txt."
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
