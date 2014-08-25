from django.db import models

class Node(models.Model):
	""" An instance of a node is a fuzzing session
	"""

	ip = models.CharField(max_length = 17)
	start_time = models.CharField(max_length = 30)
	iteration = models.CharField(max_length = 30)
	active = models.BooleanField(default = False)
	faults = models.IntegerField(default = 0)


class Crash(models.Model):
	""" Store some basic crash information with a FK to its 
	respective node
	"""

	fault_index = models.IntegerField(default = 0)
	node_index = models.ForeignKey(Node)
	crash_time = models.TextField()
	exception_type = models.TextField(default = "UNKNOWN")
	classification = models.TextField(default = "UNKNOWN")