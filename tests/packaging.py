# -*- coding: utf-8 -*-
"""Tests around project's distribution and packaging."""
import os
import unittest


tests_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(tests_dir)
build_dir = os.path.join(project_dir, 'var', 'docs', 'html')


class VersionTestCase(unittest.TestCase):
    """Various checks around project's version info."""
    def get_version(self):
        """Return xal.__version__."""
        from xal import __version__
        return __version__

    def test_version_present(self):
        """:PEP:`396` - xal has __version__ attribute."""
        try:
            self.get_version()
        except ImportError:
            self.fail('xal package has no __version__.')

    def test_version_match(self):
        """xal.__version__ matches pkg_resources info."""
        try:
            import pkg_resources
        except ImportError:
            self.fail('Cannot import pkg_resources module. It is part of '
                      'setuptools, which is a dependency of '
                      'xal.')
        distribution = pkg_resources.get_distribution('xal')
        installed_version = distribution.version
        self.assertEqual(installed_version, self.get_version(),
                         'Version mismatch: xal.__version__ '
                         'is "%s" whereas pkg_resources tells "%s". '
                         'You may need to run ``make develop`` to update the '
                         'installed version in development environment.'
                         % (self.get_version(), installed_version))

    def test_version_file(self):
        """xal.__version__ matches VERSION file info."""
        version_file = os.path.join(project_dir, 'VERSION')
        file_version = open(version_file).read().strip()
        self.assertEqual(file_version, self.get_version(),
                         'Version mismatch: xal.__version__ '
                         'is "%s" whereas VERSION file tells "%s". '
                         'You may need to run ``make develop`` to update the '
                         'installed version in development environment.'
                         % (self.get_version(), file_version))


class ReadMeTestCase(unittest.TestCase):
    """Test suite around README file."""
    def test_readme_build(self):
        """README builds to HTML without errors."""
        # Run build.
        import docutils.core
        import docutils.io
        source = open(os.path.join(project_dir, 'README')).read()
        writer_name = 'html'
        import sys
        from StringIO import StringIO
        stderr_backup = sys.stderr
        sys.stderr = StringIO()
        output, pub = docutils.core.publish_programmatically(
            source=source,
            source_class=docutils.io.StringInput,
            source_path=None,
            destination_class=docutils.io.StringOutput,
            destination=None,
            destination_path=None,
            reader=None,
            reader_name='standalone',
            parser=None,
            parser_name='restructuredtext',
            writer=None,
            writer_name=writer_name,
            settings=None,
            settings_spec=None,
            settings_overrides=None,
            config_section=None,
            enable_exit_status=False)
        sys.stderr = stderr_backup
        errors = pub._stderr.stream.getvalue()
        # Check result.
        self.assertFalse(errors, "Docutils reported errors while building "
                                 "readme content from reStructuredText to "
                                 "HTML. So PyPI would display the readme as "
                                 "text instead of HTML. Errors are:\n%s"
                                 % errors)
