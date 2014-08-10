#!/usr/bin/env python

import re
import os
import sys
import time
import jinja2
import argparse
import subprocess

environment = jinja2.Environment(loader=jinja2.FileSystemLoader('/Users/eric/src/gitblog/templates/'))

class Commit(object):
    def __init__(self, hexdigest):
        self.hexdigest = hexdigest.strip()
        data = subprocess.check_output(['git', 'cat-file', '-p', self.hexdigest])
        headers, body = data.split('\n\n', 1)
        self.body = body.strip()
        self.headers = {}
        for header in headers.split('\n'):
            k, v = header.split(' ', 1)
            self.headers[k] = v

class Post(object):
    def __init__(self, commit, args):
        self.commit = commit
        self.args = args
        (self.title, self.body) = self.commit.body.split('\n\n', 1)

    def timestamp(self):
        """
        Return a time.struct_time of the commit's author timestamp.
        """
        header = self.commit.headers['author']
        epoch, tz = re.search('(\d+) ([-+]\d{4})$', header).groups()
        return time.localtime(int(epoch))

    def slug(self):
        """
        Return a slug of the commit message's first line.
        """
        slug = re.sub('[^\w-]', '-', self.title)
        slug = re.sub('--+', '-', slug)
        slug = re.sub('(-$|^-)', '', slug)
        return slug.lower()

    def path(self):
        return '%s/%s.html' % (time.strftime('%Y/%m/%d', self.timestamp()),
                               self.slug())

    def render(self):
        destination = os.path.join(self.args.output, self.path())
        if not os.path.isdir(os.path.dirname(destination)):
            os.makedirs(os.path.dirname(destination))

        with open(destination, 'w') as html:
            template = environment.get_template('post.html')
            content = template.render(
                title=self.title,
                body=self.body,
                commit=self.commit,
            )
            html.write(content)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output', default='html')
    args = parser.parse_args()

    for hexdigest in sys.stdin:
        c = Commit(hexdigest)
        p = Post(c, args)
        p.render()

if __name__ == '__main__':
    main()
