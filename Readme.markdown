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

There are some parts of the Tumblr templating system that are not implemented
currently. Support for some of them may come later, while others would require
more information than is currently provided by the API.

* Pagination isn't accurately rendered

    `{block:NextPage}` isn't rendered, `{CurrentPage}` is fixed at 1, and
    `{TotalPages}` is fixed at 15

* `{TagsAsClasses}` doesn't add the 'reblog' class as we don't get reblog info
  from the API

* `{block:Post[1-15]}` aren't rendered

* `{block:More}` isn't rendered

    Read More breaks aren't in the API feed. I think. I've never used the Read
    More feed.

* Quote `{Length}` is fixed at 'long'

    I need to figure out what logic Tumblr uses for determining quote length.

* Photosets are only rendered as their first photo. This is a combination of
  oddities in the API and not being given the code to generate the slideshow. I
  could generate the embed code, but it would be a bit hacky at this point.

* Chat `{UserNumber}` isn't included in the API. Is it even used internally?

* Audio `{FormattedPlays}` currently simply returns the unformatted play count.

* `{Beats}` in the time. Because, seriously.

* Note information isn't rendered

    The API provides no way to access notes for a post. To make designing
    easier, Rendr currently displays a random note count for each post.

* All of the custom meta-tag-based tags aren't rendered, or even filtered out.

    This could be added in the future, just requires parsing the theme more
    robustly than I'm currently doing

* Multiple Authors aren't rendered

    The API doesn't include post author information. The ignored tags include:
    
    * `{block:GroupMembers}`
    * `{block:GroupMember}`
    * `{GroupMemberName}`
    * `{GroupMemberTitle}`
    * `{GroupMemberURL}`
    * `{GroupMemberPortraitURL-16}`
    * `{GroupMemberPortraitURL-24}`
    * `{GroupMemberPortraitURL-30}`
    * `{GroupMemberPortraitURL-40}`
    * `{GroupMemberPortraitURL-48}`
    * `{GroupMemberPortraitURL-64}`
    * `{GroupMemberPortraitURL-96}`
    * `{GroupMemberPortraitURL-128}`
    * `{PostAuthorName}`
    * `{PostAuthorTitle}`
    * `{PostAuthorURL}`
    * `{PostAuthorPortraitURL-16}`
    * `{PostAuthorPortraitURL-24}`
    * `{PostAuthorPortraitURL-30}`
    * `{PostAuthorPortraitURL-40}`
    * `{PostAuthorPortraitURL-48}`
    * `{PostAuthorPortraitURL-64}`
    * `{PostAuthorPortraitURL-96}`
    * `{PostAuthorPortraitURL-128}`

* Anything relating to permalink pages is currently not rendered.

    This includes:
    
    * `{block:PermalinkPage}`
    * `{block:PostTitle}`
    * `{PostTitle}`
    * `{block:PostSummary}`
    * `{PostSummary}`
    * `{block:PermalinkPagination}`
    * `{block:PreviousPost}`
    * `{block:NextPost}`
    * `{PreviousPost}`
    * `{NextPost}`
    * `{block:PostNotes}`
    * `{PostNotes}`

* Day pages aren't supported

    This includes filtering out the following tags:
    
    * `{block:DayPage}`
    * `{block:DayPagination}`
    * `{block:PreviousDayPage}`
    * `{block:NextDayPage}`
    * `{PreviousDayPage}`
    * `{NextDayPage}`
    
* Tag pages aren't supported

    This includes filtering out the following tags:
    
    * `{block:TagPage}`
    * `{Tag}`
    * `{URLSafeTag}`
    * `{TagURL}`
    * `{TagURLChrono}`

* Search pages aren't supported

    This includes filtering out the following tags:

    * `{block:SearchPage}`
    * `{block:NoSearchResults}`
    * `{SearchQuery}`
    * `{URLSafeSearchQuery}`
    * `{SearchResultCount}`

* Following lists aren't supported. The API does not provide this information.

    This includes filtering out the following tags:
    
    * `{block:Following}`
    * `{block:Followed}`
    * `{FollowedName}`
    * `{FollowedTitle}`
    * `{FollowedURL}`
    * `{FollowedPortraitURL-16}`
    * `{FollowedPortraitURL-24}`
    * `{FollowedPortraitURL-30}`
    * `{FollowedPortraitURL-40}`
    * `{FollowedPortraitURL-48}`
    * `{FollowedPortraitURL-64}`
    * `{FollowedPortraitURL-96}`
    * `{FollowedPortraitURL-128}`


* Liked posts aren't supported. The API does not provide this information.

    This includes filtering out the following tags:

    * `{block:Likes}`
    * `{Likes}`
    * `{Likes limit="5"}`
    * `{Likes width="200"}`
    * `{Likes summarize="100"}`


* Twitter integration isn't supported. `{block:Twitter}` and `{Twitter}` are
  filtered out

* `{CustomCSS}` isn't currently rendered

  Custom CSS isn't provided by the API

* `{Favicon}`, `{PortraitURL-16}`, `{PortraitURL-24}`, `{PortraitURL-30}`,
`{PortraitURL-40}`, `{PortraitURL-48}`, `{PortraitURL-64}`,
`{PortraitURL-96}`, and `{PortraitURL-128}` aren't rendered

  No access to the avatar URL in the API.

* Reblog information isn't rendered

  Including:

  * `{block:RebloggedFrom}`
  * `{ReblogParentName}`
  * `{ReblogParentTitle}`
  * `{ReblogParentURL}`
  * `{ReblogParentPortraitURL-16}`
  * `{ReblogParentPortraitURL-24}`
  * `{ReblogParentPortraitURL-30}`
  * `{ReblogParentPortraitURL-40}`
  * `{ReblogParentPortraitURL-48}`
  * `{ReblogParentPortraitURL-64}`
  * `{ReblogParentPortraitURL-96}`
  * `{ReblogParentPortraitURL-128}`
  * `{ReblogRootName}`
  * `{ReblogRootTitle}`
  * `{ReblogRootURL}`
  * `{ReblogRootPortraitURL-16}`
  * `{ReblogRootPortraitURL-24}`
  * `{ReblogRootPortraitURL-30}`
  * `{ReblogRootPortraitURL-40}`
  * `{ReblogRootPortraitURL-48}`
  * `{ReblogRootPortraitURL-64}`
  * `{ReblogRootPortraitURL-96}`
  * `{ReblogRootPortraitURL-128}`

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
