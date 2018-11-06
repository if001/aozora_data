#!/bin/bash
SRC_FILE=$1
OUT_FILE=$2
# sed -e 's/^/BOS /g' -e 's/$/ EOS/g' $SRC_FILE > $OUT_FILE
sed -e 's/$/ EOS/g' $SRC_FILE > $OUT_FILE
