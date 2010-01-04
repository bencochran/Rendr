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

License
-------

Rendr is made available under the terms of the MIT License.

Copyright (c) 2010 Ben Cochran

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
