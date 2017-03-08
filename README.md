# auraio

A system to convey information using atmospheric lighting provided by 
an RGB LED strip connected to a Raspberry Pi.

## Install

Requires: Python 3

### Setup a Virtual Environment

`python -m venv /path/to/venvs/auraio`

### Install

`python setup.py install`

## Configure

### Example supervisord INI

    [program:auraio]
    command=auraio
    autorestart=true
    stderr_events_enabled=true
    stdout_events_enabled=true
    redirect_stderr=true
