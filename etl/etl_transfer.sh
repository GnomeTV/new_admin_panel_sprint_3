#!/usr/bin/env bash

set -e

python set_elk_schema.py
python elastic_from_postgres.py