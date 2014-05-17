# Minga - Minimal runtime Jinja2 templating for Docker and command line


You want to make a runtime configurable Docker container in the spirit of [The Twelve-Factor App](http://12factor.net) so you start moving all your config into environment variables. But this gets out of control really quickly as there is no structure and every time you use the ENV command Docker helpfully creates a new layer which can be slow and there are limits to the number you can have.

On top of this, many apps have static config files that can't read environment variables dynamically. So you whip out your regex skills and start search and replacing files all over the place.

## The Minga way

In your dockerfile you just have one environment variable per app containing JSON data. You then run Minga in a startup script before your app and give it the path to you Jinja2 templates and the JSON data to pass to those variables.

Here is my attempt to copy the chef nginx cookbook attributes. You can see the Dockerfile in my [centos-nginx](https://github.com/dlip/dockerfiles/tree/master/centos-nginx) repository.

```
ENV NGINX_DEFAULT_OPT {\ 
  "user":  "nginx",\ 
  "gzip": {\ 
    "enabled":  "on",\ 
    "static":  "off",\ 
    "http_version":  "1.0",\ 
    "comp_level":  "2",\ 
    "proxied":  "any",\ 
    "vary":  "off",\ 
    "buffers": null,\ 
    "min_length":  "1000",\ 
    "disable":  "MSIE [1-6]\\.",\ 
    "types": [\ 
      "text/plain",\ 
      "text/css",\ 
      "application/x-javascript",\ 
      "text/xml",\ 
      "application/xml",\ 
      "application/rss+xml",\ 
      "application/atom+xml",\ 
      "text/javascript",\ 
      "application/javascript",\ 
      "application/json",\ 
      "text/mathml"\ 
    ] \ 
  },\ 
 
  "sendfile" : "off"\ 
 }

```

Now we have some structure the next problem is how to override a couple of these without having to declare the whole array again. Minga takes 2 arrays, and merges them together so you can just add a 2nd environment variable with the overrides.

```
ENV NGINX_OPT {\ 
  "user":  "foo"\ 
 }

```

Or from the command line

```
docker run -e 'NGINX_OPT={"user": "foo"}' nginx
```



## Dependencies

* Python 2.6 or above
* [Jinja2](http://jinja.pocoo.org)

## Installation

You can use it as a command by adding it to your system path.

```sh
RUN curl https://raw.githubusercontent.com/dlip/minga/master/minga.py > /usr/bin/minga && chmod +x /usr/bin/minga 
```

## Usage

```sh
minga layoutDir templateDir outputDir [JsonDefaultOptions] [JsonOptions]
```
* layoutDir - This is the folder of layouts that you can import into your templates using the Jinja2 'extends' command. If you don't need this just set it to the same as templateDir.
* templateDir - Contains your Jinja2 templates. JSON data will be passed to these templates. You can have subdirectories and the structure will be used when compiling to the outputDir. You can optionally use a .jinja extension on your files and it will be removed on the target file.
* outputDir - Templates will be outputted here. Existing files will be overwriten.
* JsonDefaultOptions (Optional) - JSON string passed to the templates as a python dictionary.
* JsonOptions (Optional) - A JSON string that will override the default options.

In your docker startup script use something like the following:

```sh
bash -c "minga /etc/minga/nginx/layout /etc/minga/nginx/template /etc/nginx '$NGINX_DEFAULT_OPT' '$NGINX_OPT'" 
```
