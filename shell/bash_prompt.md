# 自定义 bash shell 的提示信息

## 准备工作
以下所有命令的执行，都是以用户 tianya 身份执行，对应你本人的机器时，请更改对应的用户名。在自定义 bash shell 提示信息前，首先需要确认你所使用的 shell 是 bash shell。执行以下命令即可：

```
less /etc/passwd | grep 'tianya'
```

若最后一个字段属性是 “/bin/bash" ，表示当前是 bash shell,如下：

```
tianya:x:1000:1000:tianya,,,:/home/tianya:/bin/bash
```

若不是，请使用 sudo 权限更改为 /bin/bash:

```
sudo vi /etc/passwd
```

修改之后，请退出，重新登录。

## 查看当前配置
在自定义之前，先了解机器上 bash shell 提示信息的默认配置。Bash shell 的提示信息是通过 PS1 和 PS2 两个环境变量设置的。

PS1 定义了基础的提示信息，每当打开 shell 时所看到的提示信息就是通过 PS1 定义的。ubuntu 默认的提示信息格式如下：

```
username@hostname: current_directory$
```

注意，符号 $ 表示当前 shell 为用户级别的 shell ，当切换到 root 时，会变为 # 符号。

PS2 用于定义多行命令的格式。可以通过一下命令查看当前的 PS2 变量的设置：

```
echo \
```

ubuntu 中 PS2 默认是 > 。

在 ubuntu 中，PS1 和 PS2 变量通过都保存在 ~/.bash.rc 文件，ubuntu 14.4 的默认设置如下：

```
# uncomment for a colored prompt, if the terminal has the capability; turned
# off by default to not distract the user: the focus in a terminal window
# should be on the output of commands, not on the prompt
#force_color_prompt=yes

if [ -n "$force_color_prompt" ]; then
    if [ -x /usr/bin/tput ] && tput setaf 1 >&/dev/null; then
        # We have color support; assume it's compliant with Ecma-48
        # (ISO/IEC-6429). (Lack of such support is extremely rare, and such
        # a case would tend to support setf rather than setaf.)
        color_prompt=yes
    else
        color_prompt=
    fi
fi

if [ "$color_prompt" = yes ]; then
    PS1='${debian_chroot:+($debian_chroot)}\[\033[01;31m\]\u@\h\[\033[31m\]:\[\033[01;31m\]\w\[\033[31m\]\$ '
else
    PS1='${debian_chroot:+($debian_chroot)}\u@\h:\w\$ '
fi
unset color_prompt force_color_prompt
```

根据代码的基本逻辑显示，若我们需要使用带颜色的提示信息，需要将取消 force_color_prompt=yes 的注释，如下所示：

```
force_color_prompt = yew
```

接着我们重点关心 bash shell 提示信息的逻辑设置：

```
if [ "$color_prompt" = yes ]; then
    PS1='${debian_chroot:+($debian_chroot)}\[\033[01;31m\]\u@\h\[\033[31m\]:\[\033[01;31m\]\w\[\033[31m\]\$ '
else
    PS1='${debian_chroot:+($debian_chroot)}\u@\h:\w\$ '
fi
unset color_prompt force_color_prompt
```

先从简单的设置看起，else 部分的语句就是 bash shell 提示信息的默认设置，在此了解一个各符号所代表的含义：

${debian_chroot:+($debian_chroot)}，表示当切换到 root shell 时，给出提示（$ -> #)。

剩下的 \u@\h:\w\$ ，是一些特殊的代指符号，以下列出 常用的符号：

- /d ：代表日期，格式为weekday month date，例如："Mon Aug 1"
- /H ：完整的主机名。
- /h ：主机名缩写。
- /t ：显示时间为24小时格式，如：HH：MM：SS
- /T ：显示时间为12小时格式
- /A ：显示时间为24小时格式：HH：MM
- /u ：当前用户的账号名称
- /v ：BASH的版本信息
- /w ：完整的工作目录名称。 home 目录会以 ~代替
- /W ：利用basename取得工作目录名称，所以只会列出最后一个目录
- /# ：下达的第几个命令
- /$ ：提示字符，如果是root时，提示符为：# ，普通用户则为：$

## 带颜色的提示符
如需要在某个特殊符号上添加颜色显示，请在前面添加 \[\033[<span style="color:red">color_infomation</span>m\],当中 color_infomation 可以取以下值：

- 30: Black
- 31: Red
- 32: Green
- 33: Yellow
- 34: Blue
- 35: Purple
- 36: Cyan
- 37: White


## 附录：
更加全面的信息，请查看 https://www.digitalocean.com/community/tutorials/how-to-customize-your-bash-prompt-on-a-linux-vps


## 显示机器 ip

```
IP=$(ifconfig eth0 | awk ' /inet addr:/  { print $2 } ' | cut -c6- )
if test -z "$IP"
then
        IP=$(hostname | awk -F. ' { print $1 } ')
fi
export IP
```
export PS1="[\u@$IP \w\$]"
