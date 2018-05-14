#!/bin/sh
# ./all_in_one.sh <authorId> <save file name>
#ダウンロードを飛ばしたい場合は、
#python3 get_aozora.pyをスキップさせ、
#<re>のついたファイルを全て削除しておく

# 江戸川乱歩 1779
# 夢野久作 96
# 大阪圭吉 236
# 小栗虫太郎 125 *
# 海野十三 160 *



if [ $# -ne 2 ] ; then
    echo "invalid argument"
    echo "./all_in_one.sh <authorId> <save file name>"
    exit 1
fi

authorId=$1
savefile=$2

# echo "start get_aozora.py"
# python3 get_aozora.py -i $1 -e 57226 57227 57165 57230 57105
# if [ $? -ne 0 ]; then
#     echo "get_aozora.py error"
#     exit 1
# fi

echo "start unzip_somefile.sh"
./unzip_somefile.sh
if [ $? -ne 0 ]; then
    echo "unzip_somefile.sh error"
    exit 1
fi
echo "rm png"
rm *.png


echo "to utf8"
in_prefix=""
out_prefix="utf8_"
./convert_utf8.sh $in_prefix $out_prefix
if [ $? -ne 0 ]; then
    echo "./convert_utf8.sh error"
    exit 1
fi
rm_files=`ls | grep -v ^\${in_prefix}.* | grep .txt`
# rm $rm_files


echo "start replace.sh"
in_prefix="utf8_"
out_prefix="replace_"
./replace.sh ${in_prefix} ${out_prefix}
if [ $? -ne 0 ]; then
    echo "./replace.sh error"
    exit 1
fi
rm_files=`ls | grep -v ^\${out_prefix}.* | grep .txt`
rm $rm_files


echo "start mecab_text.sh"
in_prefix="replace_"
out_prefix="mecab_"
./mecab_text.sh ${in_prefix} ${out_prefix}
if [ $? -ne 0 ]; then
    echo "./mecab_text.sh error"
    exit 1
fi
rm_files=`ls | grep -v ^\${out_prefix}.* | grep .txt`
rm $rm_files



echo "reshape_text.py "
in_prefix="mecab_"
out_prefix="pyreshape_"
python3 reshape_text.py $in_prefix $out_prefix
if [ $? -ne 0 ]; then
    echo "reshape_text.py error"
    exit 1
fi
rm_files=`ls | grep -v ^\${out_prefix}.* | grep .txt`
rm $rm_files


in_prefix="pyreshape_"
out_prefix="files_all_"
./linking_text.sh $in_prefix $out_prefix $savefile
if [ $? -ne 0 ]; then
    echo "./linking_text.sh error"
    exit 1
fi
rm_files=`ls | grep -v ^\${out_prefix}.* | grep .txt`
rm $rm_files

# rm re_* 
mv *.zip ./zip
#rm *.png
exit 0
