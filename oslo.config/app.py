
from oslo.config import cfg

opt_group = cfg.OptGroup(
    name='simple',
    title='a simple example'
)

simple_opts = [
    cfg.BoolOpt('enable', default=False, help=('True, enable; False, disable'))
]

CONF = cfg.CONF
CONF.register_group(opt_group)
CONF.register_opts(simple_opts, opt_group)

if __name__ == '__main__':
    CONF(default_config_files=['app.conf'])
    print(CONF.simple.enable)
#    print(CONF.simple)

