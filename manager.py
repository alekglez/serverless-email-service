# -*- coding: utf-8 -*-

import unittest

import click
import coverage


@click.group()
def cli_main():
    """ App main entry point. """


@click.group()
def cli_test():
    """ Tests entry point. """


@cli_test.command('test')
def test():
    """ Runs the test without generating a coverage report """

    tests = unittest.TestLoader().discover("email_service", pattern="test*.py")
    result = unittest.TextTestRunner(verbosity=2).run(tests)

    if result.wasSuccessful():
        return True
    return False


@cli_test.command('coverage')
def cov():
    """ Runs the unit tests and generates a coverage report on success """

    coverage_ = coverage.coverage(branch=True, include=["./email_service/*"])
    tests = unittest.TestLoader().discover("email_service", pattern="test*.py")
    coverage_.start()
    
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        coverage_.stop()
        coverage_.save()

        print("Coverage Summary:")
        coverage_.report()
        coverage_.html_report()
        coverage_.erase()
        return True

    return False


cli = click.CommandCollection(sources=[cli_main, cli_test])
if __name__ == "__main__":
    cli()
