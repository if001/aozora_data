#! /bin/sh

files=`ls | grep .*zip`
if [ ${#files[@]} -eq 0 ]; then
    exit 1
fi

echo "unzip.sh"
for file in $files
do
    echo $file
    unzip -o $file
done

exit 0


