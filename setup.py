from distutils.core import setup
setup(
  name = 'gadrionwrap',         # How you named your package folder (MyLib)
  packages = ['gadrionwrap'],   # Chose the same as "name"
  version = '0.6',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Text wrapper for PIL/Pillow',   # Give a short description about your library
  author = 'gadrion',                   # Type in your name
  author_email = 'gradrionpr@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/gadr1on/gadrionwrap',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/gadr1on/gadrionwrap/archive/v_06.tar.gz',
  keywords = ['pilwrapper', 'wrapper', 'pil', 'pillow', 'pillowwrapper'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'Pillow',
          'imageedit',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ]
)
