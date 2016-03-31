https://github.com/openstack/oslo.rootwrap
http://docs.openstack.org/developer/oslo.rootwrap/
# git clone git@github.com:openstack/oslo.rootwrap.git

让其它OpenStack服务以root身份执行shell命令

以 nova 做为例子
setup.cfg
[entry_points]
console_scripts =
    nova-all = nova.cmd.all:main
    ...
    nova-rootwrap = oslo_rootwrap.cmd:main
    nova-rootwrap-daemon = oslo_rootwrap.cmd:daemon
    
运行命令
    sudo nova-rootwrap /etc/nova/rootwrap.conf COMMAND_LINE
配置sudoers文件
    

    
rootwrap.conf
    copy from /etc/nova/rootwrap.conf
    ini格式存放
    filters_path

rootwrap.d 中的filter文件
Filter名: Filter类, [Filter类参数1, Filter类参数2, ...]
Filter类型
CommandFilter
    kpartx: CommandFilter, kpartx, root
    mount: CommandFilter, mount, root
RegExpFilter
    blockdev: RegExpFilter, blockdev, root, blockdev, (--getsize64|--flushbufs), /dev/.*
    ln: RegExpFilter, ln, root, ln, --symbolic, --force, /dev/mapper/.*, .*
        ln --symbolic --force /dev/mapper/.* .*
        翻译过来就是这样
        ln --symbolic --force /dev/mapper/.test .test   (.test是假定的文件名)
        -s, --symbolic              make symbolic links instead of hard links
        -f, --force                 remove existing destination files
PathFilter
EnvFilter
...
