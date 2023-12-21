def install_plugin():
    import os
    import shutil

    import maestrowf
    import maestrowf_entk
    maestro_pth = maestrowf.__path__[0]
    plugin_pth = maestrowf_entk.__path__[0]

    print(f"This is maestros path with the new way to find it: {maestro_pth}")
    os.system(f'patch {maestro_pth}/maestro.py {plugin_pth}/maestrowf_entk.patch')

    print(f"This is plugins path with the new way to find it: {plugin_pth}")
    shutil.copy(f'{plugin_pth}/backend_entk.py', maestro_pth)
