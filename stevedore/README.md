# thinking stevedore #
Manage dynamic plugins for Python applications
based on setuptools

format
name = module:importable

## 1. 插件实现 ##
ceilometer/compute/virt/virt/inspector.py
ceilometer/compute/virt/libvirt/inspector.py

## 2. 插件注册 ##
ceilometer/setup.cfg
    [entry_points]
    ceilometer.compute.virt =
        libvirt = ceilometer.compute.virt.libvirt.inspector:LibvirtInspector
        hyperv = ceilometer.compute.virt.hyperv.inspector:HyperVInspector
        vsphere = ceilometer.compute.virt.vmware.inspector:VsphereInspector
        xenapi = ceilometer.compute.virt.xenapi.inspector:XenapiInspector
       
## 3. 插件载入 ##
ceilometer/compute/virt/inspector.py
    get_hypervisor_inspector()
