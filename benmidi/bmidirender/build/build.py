import sys
sys.path.append('..')
import os
os.chdir('..')

sys.path.append(r'C:\Python25\Lib\site-packages\PIL')
sys.path.append('bmidilib')
sys.path.append('scoreview')

from distutils.core import setup
import py2exe

# enter the filename of your code file to compile
filename = "main.py"

# the filename of your .exe file in the dist folder
distribution = 'bmidi_to_wave'

# if run without args, build executables
if len(sys.argv) == 1:
	sys.argv.append("py2exe")

class Target:
	def __init__(self, **kw):
		self.__dict__.update(kw)
		# for the versioninfo resources, edit to your needs
		self.version = "1.1"
		self.company_name = "Ben Fisher"
		self.copyright = "GPL v2"
		self.name = "Bmidi To Wave"

################################################################
# The manifest will be inserted as resource into your .exe.  This
# gives the controls the Windows XP appearance 
#
# Another option would be to store it in a file named
# test_wx.exe.manifest, and copy it with the data_files option into
# the dist-dir.
#
manifest_template = '''
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
<assemblyIdentity
	version="5.0.0.0"
	processorArchitecture="x86"
	name="%(prog)s"
	type="win32"
/>
<description>%(prog)s Program</description>
<dependency>
	<dependentAssembly>
		<assemblyIdentity
			type="win32"
			name="Microsoft.Windows.Common-Controls"
			version="6.0.0.0"
			processorArchitecture="X86"
			publicKeyToken="6595b64144ccf1df"
			language="*"
		/>
	</dependentAssembly>
</dependency>
</assembly>
'''

RT_MANIFEST = 24

# description is the versioninfo resource
# script is the code file
# manifest_template is the above XML code
# distribution will be the exe filename
# icon_resource is optional, remove any comment and give it an iconfile you have
#   otherwise a default icon is used
# dest_base will be the exe filename
test_wx = Target(
	description = "Pythonpixels",
	script = filename,
	other_resources = [(RT_MANIFEST, 1, manifest_template % dict(prog=distribution))],
	dest_base = distribution)

################################################################

setup(
	options = {"py2exe": {"compressed": 1,
						  "optimize": 2,
						  "ascii": 1,
						  }},
	zipfile = None,    
	windows = [test_wx],
	
	py_modules=[
		'scoreview\\__init__',
		'scoreview\\scoreview',
		'scoreview\\scoreview_util',
		'scoreview\\listview',
		'scoreview\\drawmidis',

		 'midirender_audiooptions',
		 'midirender_choose_midi_voice',
		 'midirender_consoleout',
		 'midirender_mixer',
		 'midirender_playback',
		 'midirender_runtimidity',
		 'midirender_soundfont',
		 'midirender_soundfont_info',
		 'midirender_tempo',
		 'midirender_util',
		
		],
	data_files=[ 
		#( directory, [filepath])
		# instead of typing these here, just manually add all required files.
		# include the 'scoreview' and 'bmidilib' directories; they're still needed.
		],
	
	#Optional ones here
	author='Ben Fisher'
	)



