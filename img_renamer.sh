function get_help() {
    echo "renamer: usage: renamer [-s] [-r] (-s is number to start from, -r is forward or reverse renaming should be used, default is forward)"
}


if [ $1 == "--help" ]; then
    get_help
    exit
fi


while getopts "s:r:" option
do
 case "${option}"
 in
 s) start_from=${OPTARG};;
 r) renaming_type=${OPTARG};;
 esac
done


if [ "$start_from" == "" ]; then
    get_help
    exit
fi


function reverse() {
    array=(*.jpg)
    for ((i = ${#array[@]} - 1;i >= 0;i--)); do
      new=$(printf "%04d.jpg" "$start_from")
      mv -i -- "${array[i]}" "$new"
      let start_from=start_from+1
    done
}


function forward() {
    for i in *.jpg; do
      new=$(printf "%04d.jpg" "$start_from")
      mv -i -- "$i" "$new"
      let start_from=start_from+1
    done
}


if [ "$renaming_type" == "reverse" ]; then
    reverse
else
    forward
fi
