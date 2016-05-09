import numpy as np
import sys

class Team:
    def __init__(self, proj_pa, proj_hr, team_id, ytd_hr = 0):
        self.proj_pa = proj_pa
        self.proj_hr = proj_hr
        self.team_id = team_id
        self.ytd_hr = ytd_hr

    def __repr__(self):
        return "TeamId: %s ProjPA: %s ProjHR: %s YtdHR: %s\n" % (self.team_id, self.proj_pa, self.proj_hr, self.ytd_hr)

def simulate_ros_hr(num_pa, num_hr):
    chance_of_hr = num_hr/float(num_pa)
    pa_list = np.random.rand(num_pa,1)

    return(sum(pa_list < chance_of_hr))

teams_list = []

dt=np.dtype([('league','S2'), ('team_abbrev','S3'),('ros_pa', int), ('ros_hr', int), ('ytd_hr', int)])
ros_hr_file = np.loadtxt('..\\data\\ros_hr.csv', delimiter=",", skiprows=1, dtype=dt)
ros_hra_file= np.loadtxt('..\\data\\ros_hra.csv', delimiter=",", skiprows=1,dtype=dt)

offense = False
if offense:
    for row in ros_hr_file:
        teams_list.append(Team(row[2], row[3], row[1], ytd_hr=row[4]))
else:
    for row in ros_hra_file:
        teams_list.append(Team(row[2], row[3], row[1], ytd_hr=row[4]))

team_total = {}
highest_count = {}
lowest_count = {}
num_sims = 10000

print teams_list

for sim in range(0, num_sims):
    print("Sim #", sim)
    min_hr = sys.maxint
    min_hr_teams = []

    max_hr = 0
    max_hr_teams = []

    for team in teams_list:
        season_total_hr = simulate_ros_hr(team.proj_pa, team.proj_hr) + team.ytd_hr

        if season_total_hr > max_hr:
            max_hr = season_total_hr
            max_hr_teams = [team.team_id]
        elif season_total_hr == max_hr:
            max_hr_teams.append(team.team_id)

        if season_total_hr < min_hr:
            min_hr = season_total_hr
            min_hr_teams = [team.team_id]
        elif season_total_hr == min_hr:
            min_hr_teams.append(team.team_id)

    for lead_team in max_hr_teams:
        if lead_team in highest_count:
            highest_count[lead_team] = highest_count[lead_team] + 1
        else:
            highest_count[lead_team] = 1

    for low_team in min_hr_teams:
        if low_team in lowest_count:
            lowest_count[low_team] = lowest_count[low_team] + 1
        else:
            lowest_count[low_team] = 1


print("high",highest_count)
print("low",lowest_count)

