#!/usr/bin/env python

import re
import sys
import time
import subprocess

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
    def __init__(self, commit):
        self.commit = commit

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
        if '\n\n' in self.commit.body:
            (title, _) = self.commit.body.split('\n\n', 1)
        else:
            title = self.commit.body
        slug = re.sub('[^\w-]', '-', title)
        slug = re.sub('--+', '-', slug)
        slug = re.sub('(-$|^-)', '', slug)
        return slug.lower()

    def path(self):
        return '%s/%s.html' % (time.strftime('%Y/%m/%d', self.timestamp()),
                               self.slug())

def main():
    for hexdigest in sys.stdin:
        c = Commit(hexdigest)
        p = Post(c)
        print (p.path(), c.hexdigest)

if __name__ == '__main__':
    main()
