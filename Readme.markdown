Rendr
=====

Rendr is a simple application to make designing [Tumblr](http://tumblr.com)
themes easier.

It allows you to specify a local theme file and a Tumblr URL. It then starts up
a local webserver, serving up that blogs contents styled with your theme. When
you reload the page the theme is reread, making it easy to view changes
immediately.

Use
---

    $ rendr http://blog.petervidani.com theme.html

Then visit [http://localhost:88625/](http://localhost:88625/) in you browser to
see the results.

Optionally, you can save the output to a file by using the `-o` option. See
`rendr --help` for more details.

Caveats
-------

Currently, only some aspects of the Tumblr templating system are implemented. I
intend to implement as much as is reasonably possible.

There are, however, some limitations of the Tumblr API that will cause some
features to not be implementable:

* **Note counts**. The API provides no way to access notes for a post. To make
  designing easier, Rendr currently displays a random note count for each post.

* **Multiple Authors**. The API doesn't include post author information.