#! /bin/sh
##
#テキストファイルをわかち
#

files=`ls | grep .*txt`
echo "mecab_text.sh"
for file in $files
do
    echo $file
    nkf -w $file > "utf8_"$file
    neologd_path="/usr/local/lib/mecab/dic/mecab-ipadic-neologd"
    if [ -e ${neologd_pathme} ]; then
	mecab -Owakati "utf8_"$file -o "re_"$file -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd
    else
	mecab -Owakati "utf8_"$file -o "re_"$file
    fi
    rm "utf8_"$file
    rm $file
done

exit 0

