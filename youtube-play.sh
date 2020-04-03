source /home/ma08/pro/repos/youplay/youvenv/bin/activate
if [ $# -eq 0 ]; then
    echo "No arguments provided" 
	urxvt --hold -e /home/ma08/pro/repos/youplay/youtube-play.py
fi
otherVar=`echo -n $1 | wc -m`   
while [ -n "$1" ]; do # while loop starts
    echo "bbbbb\n" 
    case "$1" in
	#/home/ma08/pro/repos/youplay/youtube-play.py --l \"$1\"
    -l) echo "I am lucky option passed $2" &&  urxvt --hold -e /home/ma08/pro/repos/youplay/youtube-play.py --l "$2";;
     --q)echo "I am lucky option not passed $2" &&  urxvt --hold -e /home/ma08/pro/repos/youplay/youtube-play.py --q "$2";;
	 *) [[ otherVar != 1 ]] && urxvt --hold -e /home/ma08/pro/repos/youplay/youtube-play.py --q "$1" || echo "option of $1"
    esac
    shift
done
