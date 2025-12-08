#!/bin/bash

# Wrapper script to run Jekyll from project root directory
# This ensures bundle uses the correct paths

cd /home/qzj/code/qiaozhijian.github.io
export BUNDLE_GEMFILE=./tools/Gemfile
exec bundle exec jekyll "$@"
