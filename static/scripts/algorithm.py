# Goatt algorithm for string recommendation

class Recommendation:
	# FIXME: You can do better
	AGE = ["moins de 12ans", "entre 12ans et 60ans", "plus de 60ans"]
	PLAY_FREQ = ["rarement", "parfois", "souvent"]
	BREAK_FREQ = ["rarement", "parfois", "souvent"]
	GOAL = ["confort", "solidite", "performance"]

	def __init__(self, data):
		self.age = data["age"]
		self.pf = data["play_freq"]
		self.bf = data["break_freq"]
		self.goal = data["goal"]
		self.is_injured = data["injury"]

	def is_consistent(self):
		return (self.age in self.AGE
				and self.pf in self.PLAY_FREQ
				and self.bf in self.BREAK_FREQ
				and self.goal in self.GOAL)

	def process(self):
		if not self.is_consistent():
			return None

		# Edges cases recommendation
		if self.age == self.AGE[0]:  # young player
			reco = 8
		elif self.age == self.AGE[2]:  # old player
			reco = 10
		elif self.is_injured:  # injured player
			if self.pf == self.PLAY_FREQ[0] or self.pf == self.PLAY_FREQ[1]:
				reco = 10
			else:
				reco = 7
		# Recommendation algorithm
		else:
			if self.pf == self.PLAY_FREQ[0]:
				if self.bf == self.BREAK_FREQ[0]:
					if self.goal == self.GOAL[0]:
						reco = 1
					elif self.goal == self.GOAL[1]:
						reco = 2
					elif self.goal == self.GOAL[2]:
						reco = 3
				else:  # self.bf == self.BREAK_FREQ[1] or self.bf == self.BREAK_FREQ[2]
					if self.goal == self.GOAL[0]:
						reco = 4
					elif self.goal == self.GOAL[1]:
						reco = 5
					elif self.goal == self.GOAL[2]:
						reco = 6

			if self.pf == self.PLAY_FREQ[1]:
				if self.bf == self.BREAK_FREQ[0]:
					if self.goal == self.GOAL[0]:
						reco = 3
					elif self.goal == self.GOAL[1]:
						reco = 2
					elif self.goal == self.GOAL[2]:
						reco = 3
				elif self.bf == self.BREAK_FREQ[1]:
					if self.goal == self.GOAL[0]:
						reco = 2
					elif self.goal == self.GOAL[1]:
						reco = 9
					elif self.goal == self.GOAL[2]:
						reco = 6
				elif self.bf == self.BREAK_FREQ[2]:
					if self.goal == self.GOAL[0]:
						reco = 4
					elif self.goal == self.GOAL[1]:
						reco = 5
					elif self.goal == self.GOAL[2]:
						reco = 6

			if self.pf == self.PLAY_FREQ[2]:
				if self.bf == self.BREAK_FREQ[0]:
					if self.goal == self.GOAL[0]:
						reco = 3
					elif self.goal == self.GOAL[1]:
						reco = 9
					elif self.goal == self.GOAL[2]:
						reco = 3
				else:  # self.bf == self.BREAK_FREQ[1] or self.bf == self.BREAK_FREQ[2]
					if self.goal == self.GOAL[0]:
						reco = 2
					elif self.goal == self.GOAL[1]:
						reco = 5
					elif self.goal == self.GOAL[2]:
						reco = 6

		return reco
