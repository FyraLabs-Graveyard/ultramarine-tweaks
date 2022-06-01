pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'umtweaks')
gnome = import('gnome')

gnome.compile_resources('ultramarine-tweaks',
  'umtweaks.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'ultramarine-tweaks.in',
  output: 'ultramarine-tweaks',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir')
)

umtweaks_sources = [
  'app.py',
  'pages.py',
  '__main__.py',
  'pages.py',
  'window.py',
  'widgets.py',
]

install_data(umtweaks_sources, install_dir: moduledir)

subdir('modules')