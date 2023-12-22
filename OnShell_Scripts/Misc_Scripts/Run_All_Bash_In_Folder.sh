#!/bin/bash

for f in $1*.sh; do
  bash "$f" 
done
