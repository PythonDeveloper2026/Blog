#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_project.settings')
    try:
        from django.core.management import execute_from_command_line
        
        # Monkeypatch for Python 3.14 compatibility
        import sys
        if sys.version_info >= (3, 14):
            from django.template import context
            def patched_copy(self):
                new_context = self.__class__.__new__(self.__class__)
                new_context.__dict__.update(self.__dict__)
                new_context.dicts = self.dicts[:]
                return new_context
            context.BaseContext.__copy__ = patched_copy
            context.Context.__copy__ = patched_copy
            if hasattr(context, 'RequestContext'):
                context.RequestContext.__copy__ = patched_copy
            
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
