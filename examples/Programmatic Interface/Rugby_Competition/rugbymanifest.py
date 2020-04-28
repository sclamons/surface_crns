import os,sys,random

if not len(sys.argv) == 3:
    sys.exit('must invoke with exactly two team file names.')

teams = sys.argv[1:]
team1 = sys.argv[1]
team2 = sys.argv[2]
teamname1 = team1.split('.')[0]
teamname2 = team2.split('.')[0]
manifile = 'competition_manifest_'+teamname1+"_vs_"+teamname2+'.txt'

def create_manifest(teamXfile,teamYfile):
  manifest=[]
  with open('rugby-online-manifest.txt') as fp:
    for line in fp:
        manifest.append(line)

  preamble=[]
  postscript=[]

  for line in manifest:
    preamble.append(line)
    if "team X" in line:
        break

  for line in manifest:
    if len(postscript) > 0:
        postscript.append(line)
    if "!END_TRANSITION_RULES" in line:
        postscript.append(line)

  teamX=[]
  with open(teamXfile) as fp:
    for line in fp:
        teamX.append(line.replace("Y","X"))

  teamY=[]
  with open(teamYfile) as fp:
    for line in fp:
        teamY.append(line.replace("X","Y"))

  manifest=preamble+teamX+teamY+postscript
                     
  with open(manifile,'w') as fp:
    for line in manifest:
        fp.write(line)

create_manifest(team1,team2)



