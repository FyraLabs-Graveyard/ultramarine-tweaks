pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'umtweaks', 'modules')
gnome = import('gnome')

umtweaks_sources = [
  '__init__.py',
  'appearance.py',
  'backups.py',
  'dnf_repos.py',
  'kernel.py',
  'power.py',
]

install_data(umtweaks_sources, install_dir: moduledir)
