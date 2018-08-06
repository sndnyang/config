
cwd=`pwd`
prj=`echo "$cwd" | cut -d "/" -f 6`;

branch=`echo "$cwd" | cut -d "/" -f 5`;

if [[ $branch == "master" ]]
then
    new_pwd=`echo "$cwd" | sed 's/master/research/'`
    echo "$new_pwd"
    cd "$new_pwd"
else
    new_pwd=`echo "$cwd" | sed 's/research/master/'`
    echo "$new_pwd"
    cd "$new_pwd"
fi

