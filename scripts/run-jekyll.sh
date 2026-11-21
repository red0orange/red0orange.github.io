#!/usr/bin/env bash
set -euo pipefail
# Resolve the checkout instead of depending on a machine-specific path.
project_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$project_root"
export BUNDLE_GEMFILE="$project_root/tools/Gemfile"
exec bundle exec jekyll "$@"
