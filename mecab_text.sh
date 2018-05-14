#! /bin/sh
##
#テキストファイルをわかち
#
if [ $# -eq 2 ]; then
   in_prefix=$1
   out_prefix=$2
elif [ $# -eq 1 ]; then
    in_prefix=""
    out_prefix=$1
else
    echo "bud argument"
    exit 1
fi

files=`ls | grep ^\${in_prefix}.*\.txt`
echo "mecab_text.sh"

for file in $files
do
    echo $file
    neologd_path=/usr/local/lib/mecab/dic/mecab-ipadic-neologd
    if [ -e ${neologd_path} ]; then
	mecab -Owakati ${file} -o ${out_prefix}${file} -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd
    else
	mecab -Owakati ${file} -o ${out_prefix}${file}
    fi
done

exit 0

