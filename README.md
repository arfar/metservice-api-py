Minimal Metservice API in Python
================================

Complete rewrite as [issue 1](https://github.com/arfar/metservice-api-py/issues/1)
completely invalidated what I had done previously. Now the script will simply pull
the url and convert the JSON to a dictionary. Nothing fancy what-so-ever.

Usage
=====

Creating the url strings is up to the user, but all the required prefixes and
suffixes are already there (I'm pretty sure). Use the
`if __name__ == '__main__':` section as an example of how to construct the
webpages.

If you just want a dump of all the weather related bits, use:

    python metservice.py christchurch
    python metservice.py western-hills

Note that not all APIs will work with the smaller areas, for example WARNINGS
is a region based API and so will not work on western-hills, but will work with
wellington.

Contact Me
==========

If it's not working how you'd like feel free to email me and I'll fix it, or
send a pull request and I'll almost definitely accept it.

If you're metservice and you're not happy, please email me at: arthurlhr@gmail.com
