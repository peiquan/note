#!/bin/bash
sudo apt-get install -y --force-yes autojump git zsh

currentUsername=$(echo $USER)

# install oh-my-zsh
sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
sed -i 's/plugins=(git)/plugins=(git autojump)/g' ~/.zshrc

if grep -q "export SHELL=/bin/zsh" ~/.bashrc 
then
    echo  "already exists"
else
    echo "export SHELL=/bin/zsh" | tee -a ~/.bashrc
    echo "exec /bin/zsh -l" | tee -a  ~/.bashrc
fi

# change oh-my-zsh prompt
if [[ ! -d "/home/$currentUsername/.oh-my-zsh/custom/themes" ]]; then
  mkdir "/home/$currentUsername/.oh-my-zsh/custom/themes"
fi
if [ ! -f "/home/$currentUsername/.oh-my-zsh/custom/themes/robbyrussell.zsh-theme" ]; then
  curl https://raw.githubusercontent.com/peiquan/note/master/shell/zsh/robbyrussell.zsh-theme -L > /home/$currentUsername/.oh-my-zsh/custom/themes/robbyrussell.zsh-theme
fi

source /home/$currentUsername/.zshrc


