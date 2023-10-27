# ExpliciTag

[![Python version](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://pypi.python.org/pypi/config-formatter) [![License](https://img.shields.io/github/license/delgan/config-formatter.svg)](https://codeberg.org/frosty/explicitag/src/branch/master/LICENSE)

MP4 rating tagger based on lyrics

**Note**: this is only meant for MP4 (AAC/M4A) files, as they only have the tag that this program modifies. It's meant for iTunes to read it, and mark your tracks' ratings.

## Installation

Clone the repository:
```shell
~ git clone https://codeberg.org/frosty/explicitag
```

Go into the cloned directory:
```shell
~ cd explicitag
```

Install it using `pip`:
```shell
~ pip install .
```

## Usage

```shell
usage: explicitag [-h] path [path ...]

MP4 rating tagger based on lyrics

positional arguments:
  path        file or directory to process

options:
  -h, --help  show this help message and exit

Source code: https://codeberg.org/frosty/explicitag
```

## Examples

Using a directory as input:
```shell
D:\Projects\explicitag>py -m explicitag "D:\Files\Tagged Music\Nine Inch Nails\1989 - Pretty Hate Machine"
[10:38:25] INFO - Marked "1.01 - Head Like a Hole.m4a" as explicit
[10:38:26] INFO - Marked "1.02 - Terrible Lie.m4a" as explicit
[10:38:26] INFO - Marked "1.03 - Down in It.m4a" as explicit
[10:38:26] INFO - Marked "1.04 - Sanctified.m4a" as explicit
[10:38:26] INFO - Marked "1.05 - Something I Can Never Have.m4a" as explicit
[10:38:26] INFO - Marked "1.06 - Kinda I Want To.m4a" as explicit
[10:38:28] INFO - Marked "1.07 - Sin.m4a" as explicit
[10:38:31] INFO - Marked "1.08 - That’s What I Get.m4a" as clean
[10:38:35] INFO - Marked "1.09 - The Only Time.m4a" as explicit
[10:38:40] INFO - Marked "1.10 - Ringfinger.m4a" as explicit

Complete. 0 file(s) skipped.
```

Using a file as input:
```shell
D:\Projects\explicitag>py -m explicitag "D:\Files\Tagged Music\Tyler, the Creator\2017 - ZIPLOC\1.01 - ZIPLOC.m4a"
[10:39:02] INFO - Marked "1.01 - ZIPLOC.m4a" as explicit

Complete. 0 file(s) skipped.
```

Using a list of files (dropped from iTunes) as input:
```shell
D:\Projects\explicitag>py -m explicitag "D:\Files\Tagged Music\Burning Airlines\1999 - Mission_ Control!\1.04 - Scissoring.m4a" "D:\Files\Tagged Music\Burning Airlines\1999 - Mission_ Control!\1.05 - The Escape Engine.m4a" "D:\Files\Tagged Music\D.R.I\1989 - Thrash Zone\1.02 - Beneath the Wheel.m4a" "D:\Files\Tagged Music\The Dismemberment Plan\2001 - Change\1.02 - The Face of the Earth.m4a" "D:\Files\Tagged Music\The Dismemberment Plan\2001 - Change\1.03 - Superpowers.m4a" "D:\Files\Tagged Music\The Dismemberment Plan\1999 - Emergency & I\1.03 - What Do You Want Me to Say_.m4a" "D:\Files\Tagged Music\The Faint\2001 - Danse Macabre\1.01 - Agenda Suicide.m4a" "D:\Files\Tagged Music\The Faint\2001 - Danse Macabre\1.06 - Posed to Death.m4a" "D:\Files\Tagged Music\A Flock of Seagulls\1986 - The Best Of\1.03 - Telecommunication.m4a" "D:\Files\Tagged Music\A Flock of Seagulls\1986 - The Best Of\1.04 - The More You Live, the More You Love.m4a"
[10:39:34] INFO - Marked "1.04 - Scissoring.m4a" as explicit
[10:39:34] INFO - Marked "1.05 - The Escape Engine.m4a" as explicit
[10:39:34] INFO - Marked "1.02 - Beneath the Wheel.m4a" as explicit
[10:39:34] INFO - Marked "1.02 - The Face of the Earth.m4a" as explicit
[10:39:34] INFO - Marked "1.03 - Superpowers.m4a" as explicit
[10:39:34] INFO - Marked "1.03 - What Do You Want Me to Say_.m4a" as explicit
[10:39:34] INFO - Marked "1.01 - Agenda Suicide.m4a" as explicit
[10:39:34] INFO - Marked "1.06 - Posed to Death.m4a" as explicit
[10:39:34] INFO - Marked "1.03 - Telecommunication.m4a" as explicit
[10:39:34] INFO - Marked "1.04 - The More You Live, the More You Love.m4a" as explicit

Complete. 0 file(s) skipped.
```