# groupmestats

## Setup

You'll probably need to install `python3`.

Once you have `python3` installed, follow these instructions to get
`groupmestats` up and running.

- Make sure you have `virtualenv` installed: `pip install virtualenv`
- Create a new python virtual environment: `virtualenv -p python3 env`
- Activate the virtual environment: `source ./env/bin/activate`
- Install the required `groupmestats` module: `pip install --editable <directory containing setup.py>`
- Follow the instructions on setting up your GroupMe API key to be discoverable
  by the `groupy` module: http://groupy.readthedocs.io/en/latest/pages/installation.html
- For statistics that generate plotly plots, create an account at
  https://plot.ly/, and follow the instructions at
  https://plot.ly/python/getting-started/ to create
  `<home>/.plotly/.credentials` with your username and API key.
- On MacOS, I've had trouble with Pillow version and jpeg decoders. After
  some combination of uninstalling pillow (`pip uninstall pillow`),
  installing libjpeg via brew ('brew install libjpeg'), and then trying
  again with the installer from http://ethan.tira-thompson.com/Mac_OS_X_Ports.html,
  and finally changing editing <python env>/site-packages/GroupyAPI-0.7.1.dist-info/METADATA
  to change the line `Requires-Dist: Pillow (==2.5.3)` to `Requires-Dist: Pillow (==4.2.1)`,
  I managed to get things working.

## Fetch data from GroupMe server

After groupmestats is installed, run the command `gstat_fetch_data`
to download GroupMe group and message data to a cache on disk. All future
stats analysis will be peformed on data from this cache without making
repeated slow requests to the GroupMe servers. You can re-run
`gstat_fetch_data` at any time to update the cache.

## Generate Statistics

Run the command `gstat_stats` to generate a statistical report for your group.

## More Help

Run `gstat_help`

## (Optional) Generate and modify member and group aliases

### Group aliases
Run `gstat_gen_groups` to generate a YAML file that groupmestats will use
to correlate group names to the group's unique ID assigned by GroupMe.
This will generate `<home>/.groupmestats/groups-generated.yaml`,
containing text such as this:

    groups:
    - group_id: '15555212'
      names: [Pancake-Related Messages]

You can add names to a group so the group can be identified by multiple names.
This can also help if your group's name is changed. If you would like a group
to be known by multiple names, copy the contents of `groups-generated.yaml`
to `<home>/.groupmestats/groups.yaml` and add the additional name, e.g.:

    groups:
    - group_id: '15555212'
      names: [Pancake-Related Messages, People Talking About Pancakes]

Now you can use either `Pancake-Related Messages` or
`People Talking About Pancakes` to refer to this group.

### Member aliases
Similary, you can run `gstat_gen_members` to generate
`<home>/.groupmestats/members-generated.yaml`, e.g.:

    members:
    - {nickname: Kyle Teske, user_id: '180617'}

You can edit the nickname that shows up in statistics, which may be useful
if people change their names often, or just have weird names that you don't like. Bots don't get generated automatically, so you may have to add those
manually. Copy `members-generated.yaml` to
`<home>/.groupmestats/members.yaml` and edit `members.yaml`, e.g.:

    members:
    - {nickname: Kyle 'Cool' Teske, user_id: '180617'}
