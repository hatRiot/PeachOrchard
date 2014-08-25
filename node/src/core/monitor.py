from src.core.log import *
from src.core import node_resource as nr
from src.core import config
from src.core import utility
from time import sleep
import os


def monitor():
	"""
	"""

	# known crashes; key is idx (top level folder before crash info); value is 
	known_crashes = {}

	try:
		utility.msg("Initializing monitor for node %s..." % config.NODE_ID)

		# check monitor dir
		if not os.path.isdir(config.MONITOR_DIR):
			utility.msg("Directory %s not found" % config.MONITOR_DIR, ERROR)
			return

		#
		# prior to monitor loop, lets ensure we're synced with upstream by providing
		# current status
		#

		# update status
		nr.send_status_update()

		# grab a listing of all current crashes; set of "knowns"
		known_crashes = fetch_crashes()

		# register crashes
		nr.register_crash(known_crashes)

		# enter the mainline monitor loop
		log_hash = nr.log_hash()
		while True:

			# we only push when the hash of the status file changes, or a
			# new fault is detected

			tmp_hsh = nr.log_hash()
			if tmp_hsh != log_hash:

				# status update
				nr.send_status_update()
				log_hash = tmp_hsh

			# pull crashes and diff for new ones
			temporal_crash = fetch_crashes()
			if len(temporal_crash) != len(known_crashes):

				# we have new crashes; ship them over
				temporal_crash = list(set(temporal_crash) - set(known_crashes))
				nr.register_crash(temporal_crash)

				known_crashes += temporal_crash

			# sleep, now
			sleep(config.CHECK_INTERVAL)

	except KeyboardInterrupt:
		pass
	except Exception, e:
		utility.msg("Error during monitor: %s" % e, ERROR)


def fetch_crashes():
	""" Build a dictionary of crash indices and crash information file.  Peach will
	dump crashes out to different folders depending on their cause, such as Fault or
	NonReproducable.  Right now we don't make a distinction; simply rummage through
	these files and build a dict.
	"""

	crashes = {}
	base = config.MONITOR_DIR + '/' + config.SESSION

	# build a list of files from session root
	pot_files = []
	for (root, subFolders, files) in os.walk(base):
		for file in files:
			f = os.path.join(root, file)
			pot_files.append(f.replace('\\', '/'))

	# prune these into our dictionary
	for entry in pot_files:

		if '_description.txt' in entry:

			# found description entry, parse
			e = entry.rsplit('/', 2)
			crashes[e[1]] = entry

	return crashes