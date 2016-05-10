import numpy as np
import sys
import operator

class Team(object):
    def __init__(self, proj_pa, proj_hr, team_id, ytd_hr = 0):
        self.proj_pa = proj_pa
        self.proj_hr = proj_hr
        self.team_id = team_id
        self.ytd_hr = ytd_hr

    def __repr__(self):
        return "TeamId: %s ProjPA: %s ProjHR: %s YtdHR: %s\n" % (self.team_id, self.proj_pa, self.proj_hr, self.ytd_hr)

def simulate_ros_hr(num_pa, num_hr):
    # Simulates a season's worth of PAs, giving a HR every time num_hr/num_pa > the random uniform generated
    chance_of_hr = num_hr/float(num_pa)
    pa_list = np.random.rand(num_pa,1)

    return(sum(pa_list < chance_of_hr))

# Set these two first
offense = True
num_sims = 10

# Load csv files which contain league, team abbreviation, projected rest of season pa/hr and year to date hr
dt=np.dtype([('league','S2'), ('team_abbrev','S3'),('ros_pa', int), ('ros_hr', int), ('ytd_hr', int)])
ros_hr_file = np.loadtxt('..\\data\\ros_hr.csv', delimiter=",", skiprows=1, dtype=dt)
ros_hra_file= np.loadtxt('..\\data\\ros_hra.csv', delimiter=",", skiprows=1,dtype=dt)

teams_list = []

# Choose batting or pitching projections based on bool above.
if offense:
    for row in ros_hr_file:
        teams_list.append(Team(row[2], row[3], row[1], ytd_hr=row[4]))
else:
    for row in ros_hra_file:
        teams_list.append(Team(row[2], row[3], row[1], ytd_hr=row[4]))

team_total = {}
highest_count = {}
lowest_count = {}

#Each simulation represents a season
for sim in range(0, num_sims):
    print("Sim #", sim)

    min_hr = sys.maxint
    min_hr_teams = []

    max_hr = 0
    max_hr_teams = []

    for team in teams_list:
        # For each team which was read in simulate a season and add ytd HRs
        season_total_hr = simulate_ros_hr(team.proj_pa, team.proj_hr) + team.ytd_hr

        # Keeps track of teams who had the most.
        # If a new max is set the current team is the new leader
        # If the max is tied add the current team to the list of leaders
        if season_total_hr > max_hr:
            max_hr = season_total_hr
            max_hr_teams = [team.team_id]
        elif season_total_hr == max_hr:
            max_hr_teams.append(team.team_id)

        # Keeps track of teams who have the fewest.
        # If a new min is set the current team is the new leader
        # If the min is tied add the current team to the list of leaders
        if season_total_hr < min_hr:
            min_hr = season_total_hr
            min_hr_teams = [team.team_id]
        elif season_total_hr == min_hr:
            min_hr_teams.append(team.team_id)

    # Count how many times each team led the league
    for lead_team in max_hr_teams:
        if lead_team in highest_count:
            highest_count[lead_team] = highest_count[lead_team] + 1
        else:
            highest_count[lead_team] = 1

    # Count how many times each team had the fewest in the league
    for low_team in min_hr_teams:
        if low_team in lowest_count:
            lowest_count[low_team] = lowest_count[low_team] + 1
        else:
            lowest_count[low_team] = 1

# Sort so that the teams which led most frequently are printed first
sorted_highest = sorted(highest_count.items(), key=operator.itemgetter(1), reverse=True)
# Sort so that the teams which trailed most frequently are printed first
sorted_lowest = sorted(lowest_count.items(), key=operator.itemgetter(1), reverse=True)

# Print teams who led the most often (and how often)
print("high",sorted_highest)
# Print the number of times the Mets led
if "NYN" in highest_count:
    print("NYN high", highest_count["NYN"])
# Print teams who trailed the most often (and how often)

print("low",sorted_lowest)
# Print the number of times the Mets trailed
if "NYN" in lowest_count:
    print("NYN low", lowest_count["NYN"])

