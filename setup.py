import setuptools

if __name__ == '__main__':
    setuptools.setup(
        name="groupmestats",
        version="0.0.1",
        author="Kyle Teske",
        author_email="kjteske@gmail.com",
        description="Calculating and displaying groupme statistics",
        packages=setuptools.find_packages(),
        license='MIT',
        classifiers=[
            'License :: OSI Approved :: MIT License',
        ],
        install_requires=[
            'GroupyAPI',
            'jinja2',
            'Pillow',
            'PyYAML',
        ],
        entry_points={
            'console_scripts': [
                'gstat_fetch_data = groupmestats.groupserializer:gstat_fetch_data',
                'gstat_gen_groups = groupmestats.grouplookup:gstat_gen_groups',
                'gstat_gen_members = groupmestats.memberlookup:gstat_gen_members',
                'gstat_help = groupmestats.help:gstat_help',
                'gstat_stats = groupmestats.generatestats:gstat_stats',
            ],
        },
    )
