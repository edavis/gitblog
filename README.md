gitblog.py
==========

gitblog.py is an experimental blog engine where blog posts are stored
as git commit objects.

Demo
----

```bash
$ git init
$ git new-post # alias for "git commit --allow-empty -F -"
(reading log message from standard input)
Hello World

This is the first post in gitblog!
^D
[master (root-commit) 70b887e] Hello World
$ git show
commit 70b887e916c2ad75c0c5b4ec69b191a528387db7
Author: Eric Davis <eric@davising.com>
Date:   Sun Aug 10 20:42:28 2014 -0700

    Hello World
    
    This is the first post in gitblog!
$ git rev-list master | ./gitblog.py
$ find html -type f
html/2014/08/10/hello-world.html
$ cat html/2014/08/10/hello-world.html
<h1>Hello World</h1>

<p>This is the first post in gitblog!</p>
```

It's still in the very early stages, but I think there is promise with
it.
