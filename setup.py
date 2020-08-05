from distutils.core import setup
setup(
  name = 'pilwrapper',         # How you named your package folder (MyLib)
  packages = ['pilwrapper'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Text wrapper for PIL/Pillow',   # Give a short description about your library
  author = 'Kevin Hernandez',                   # Type in your name
  author_email = 'gradrionpr@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/gadr1on/pilwrapper',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/gadr1on/pilwrapper/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['pilwrapper', 'wrapper', 'pil', 'pillow', 'pillowwrapper'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'Pillow',
          'imageedit',
      ],
  classifiers=[
    'Development Status :: 5 - Production/Stable',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Build Tools',
    'License :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
