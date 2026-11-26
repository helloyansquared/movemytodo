#!/bin/sh
# Rebuild the site with the live IDs (all public values; no secrets here).
python3 build.py https://movemytodo.com/ \
  --ms b7c50b09-e3e0-4334-a78c-bbafc89a3beb \
  --google 26189746666-r713cmmndeb2o79sm3ia2s89e1tivmm5.apps.googleusercontent.com \
  --product pdt_0NskgwvLberpsSzV9p3sj
