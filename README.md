# ExpliciTag

![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)
![MIT license](https://img.shields.io/github/license/delgan/config-formatter.svg)

MP4 rating tagger based on lyrics.

ExpliciTag marks MP4 (AAC/M4A) files as explicit or not based on their lyrics. This is only meant for iTunes to read, nothing else will be supported. For the best experience, tag your whole library with lyrics. This does not grab any data from APIs, and relies on the tags in the files directly.

## Installation

```
pip install git+https://github.com/st0rmw1ndz/explicitag.git
```

## Usage

```
Usage: explicitag [OPTIONS] [PATHS]...

  MP4 rating tagger based on lyrics.

  Copyright (c) 2024 frosty.

Options:
  --help  Show this message and exit.
```