IP=`ifconfig eth0 | grep "inet " | cut -d : -f 2 | cut -d " " -f 1`
local ret_status="%{$fg_bold[blue]%}$IP"
PROMPT='${ret_status} %{$fg[cyan]%}%c%{$reset_color%} '
