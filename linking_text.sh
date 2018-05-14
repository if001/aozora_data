#!/bin/sh
##
#青空文庫から取ってきたテキストファイルを全て連結
##
if [ $# -eq 3 ]; then
    in_prefix=$1
    out_prefix=$2
    save=$3
else
    echo "bud argument"
    exit 1
fi

files=`ls | grep ^\${in_prefix}.*\.txt`
fname=${out_prefix}${save}.txt
echo $files
cat $files > ${fname}
mv ${fname} ./files/${fname}
exit 0
