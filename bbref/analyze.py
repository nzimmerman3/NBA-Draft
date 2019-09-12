import csv
import io

draft = {}
#pick number -> (total_points, total_rebounds, total_assists, number of entries)

avg_ppg = []
avg_rbg = []
avg_apg = []

def print_averages():
  for p, r, a in zip(avg_ppg, avg_rbg, avg_apg):
    print(str(round(p, 1)) + " " + str(round(r, 1)) + " " + str(round(a, 1)))

def generateFiles():
  all = []
  for year in range(1960, 2020):
    filename = "data/data_" + str(year) + '.csv'
    all.append(filename)

  return all

def analyze(file):
  with io.open(file, 'r', encoding="utf-8", newline='') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
      if line_count != 0:
        if line_count not in draft:
          draft[line_count] = (0, 0, 0, 0)
        draft[line_count] = (float(row[1]) + draft[line_count][0], float(row[2]) + draft[line_count][1], float(row[3]) + draft[line_count][2], draft[line_count][3] + 1)
      line_count += 1

def create_averages():
  for pos in range(1, 61):
    avg_ppg.append(draft[pos][0]/ draft[pos][3])
    avg_rbg.append(draft[pos][1]/ draft[pos][3])
    avg_apg.append(draft[pos][2]/ draft[pos][3])

def get_standout(file):
  with io.open(file, 'r', encoding="utf-8", newline='') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
      #maybe convert to z scores?

  #need avg stats at every draft position
  #best value at every position
  #best value overall

def main():
  files = generateFiles()
  for file in files:
    analyze(file)

  create_averages()

  for file in files:
    standout = get_standout(file)
    print(standout)

if __name__ == '__main__':
  main()