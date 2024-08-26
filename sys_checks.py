
import sys
import platform

OS_Flag = ''
release = platform.system() + ' ' + platform.release()
version = platform.version()

# Returns OS information and other prerequisites that may be required 
# to make suitable adaptions

if sys.platform == 'win32':
    OS_Flag = "Windows"

if sys.platform == 'darwin':
    OS_Flag = "MacOS"

print (f'''
{OS_Flag} detected
release: {release}
version: {version}
''')