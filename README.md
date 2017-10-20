# show_log

##实时(tail -f)查看日志文件

    git clone https://github.com/lpj24/show_log.git
    pip install virtualenv
    virtualenv env
    source env/bin/activate
    cd show_log
    pip install -r requirements.txt
    python app.py -path /var/log/syslog
###path 后面添加需要查看的日志文件的完整路径, 注意日志文件的权限是否可以执行tail

    sudo docker build -t="lpj24/show_log_image" .
    sudo docker run -d -p 5500:5500 -v ~/Downloads/error.log:/opt/monitor.log --name show_log lpj24/show_log_image python app.py -path /opt/monitor.log