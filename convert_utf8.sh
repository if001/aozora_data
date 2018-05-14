#!/bin/bash
if [ $# -eq 2 ]; then
   in_prefix=$1
   out_prefix=$2
   files=`ls | grep ^\${in_prefix}.\.txt`
elif [ $# -eq 1 ]; then
    in_prefix=""
    out_prefix=$1
    files=`ls | grep .\.txt`
else
    echo "bud argument"
    exit 1
fi

for file in $files
do
    echo ${out_prefix}${file}
    nkf -w $file > ${out_prefix}${file}
done

# rm_files=`ls | grep -v ^\${out_prefix}. | grep .txt`
# rm $rm_files
