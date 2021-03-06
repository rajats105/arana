#!/usr/bin/env python
# coding: utf-8

import os
import subprocess
import sys
import json
import click
from urllib.robotparser import RobotFileParser
from urllib.parse import urlsplit

@click.command()
@click.argument('url')
@click.argument('config', type=click.Path(exists=True))
@click.option(
    '--page', '-p',
    default=0,
    help='How many pages to scrape',
)
@click.option(
    '--casperjs', '-c',
    default='casperjs',
    help="Path to the casperjs script"
)
def main(url, config, page, casperjs):
    """
    \b
      __ _ _ __ __ _ _ __   __ _
     / _` | '__/ _` | '_ \ / _` |
    | (_| | | | (_| | | | | (_| |
     \__,_|_|  \__,_|_| |_|\__,_|

    Arana is a web scraper built on top of casperJS.

    \b
    Provide the scrape URL and CONFIG file as arguments
    Here's an example:
    $ arana https://jobs.apple.com/in/search config/apple.json
    """

    """
    robotstxt = parse_robotstxt(url)

    if robotstxt is False:
        sys.stderr.write(json.dumps((dict(error=True, msg='Incorrect URL'))))
        sys.exit(1)

    if robotstxt['allowed'] is False:
        sys.stderr.write(json.dumps((dict(error=True, msg='Crawling not allowed by robots.txt'))))
        sys.exit(1)
    """

    command = [
        casperjs,
        os.path.dirname(os.path.realpath(__file__)) + '/scrape.js',
        '--disk-cache=true',
        '--url={}'.format(url),
        '--crawler={}'.format(os.path.abspath(config)),
        '--page={}'.format(page),
    ]

    ret = run_casper(command)

    if ret['error']:
        sys.stderr.write(json.dumps((ret)))
        sys.exit(ret['exitcode'])

    print(ret['stdout'])

def parse_robotstxt(url):
    """
    Parse robots.txt
    """

    parsed = urlsplit(url)

    if parsed.scheme not in ['http', 'https']:
        return False

    if parsed.netloc == '':
        return False

    robot = RobotFileParser()
    robot.set_url(parsed.scheme + "://" + parsed.netloc + "/robots.txt")
    robot.read()

    return dict(
        allowed=robot.can_fetch('*', url),
        rate=robot.request_rate('*'),
        delay=robot.crawl_delay('*'),
    )

def run_casper(cmd):
    """
    Run casperJS scraper and get data back
    """
    try:
        completed = subprocess.run(
            cmd,
            cwd=os.path.dirname(os.path.realpath(__file__)) + '/..',
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except subprocess.CalledProcessError as err:
        return dict(
            error=True,
            msg=str(err),
        )

    ret = dict(
        error=False,
        message='Script run successful',
        exitcode=completed.returncode,
        stdout=completed.stdout.decode('utf-8').strip(),
        stderr=completed.stderr.decode('utf-8').strip()
    )

    if completed.returncode > 0:
        ret['message'] = 'Script exited with non zero exit status'
        ret['error'] = True

    return ret

if __name__ == "__main__":
    main()
