import scrapy
import csv
import io

class BasketballSpider(scrapy.Spider):
  name = "basketball"
  start_urls = ["https://www.basketball-reference.com/draft/"]
  total_years = []

  #key = year
  #value = list of names/points/rebounds/assists in order
  total_names = {}
  total_points = {}
  total_rebounds = {}
  total_assists = {}

  def parse(self, response):
    #adds url of each year's draft
    years = response.css('.right a::attr(href)').getall()
    for year in years:
      yield scrapy.Request(response.urljoin(year), callback=self.parse_page)

  def parse_page(self, response):
    i = response.url.find("NBA_") + 4
    year = response.url[i:i+4]

    baa_i = response.url.find("BAA_") + 4
    baa_year = response.url[baa_i:baa_i+4]

    try:
      int(year)
    except:
      year = baa_year

    names=[]
    points = []
    rebounds = []
    assists = []

    max = response.css("#all_stats h2::text").get()

    for j in range(1, int(max.split(' ')[0]) + 30):
      jay = str(j)

      search_points = "tr:nth-child(" + jay + ") .right:nth-child(16)::text"
      search_names = "tr:nth-child(" + jay + ") .left:nth-child(4) *::text"
      search_rebounds = "tr:nth-child(" + jay + ") .right:nth-child(17)::text"
      search_assists = "tr:nth-child(" + jay + ") .right:nth-child(18)::text"

      names.append(response.css(search_names).get())
      points.append(response.css(search_points).get(default='0'))
      rebounds.append(response.css(search_rebounds).get(default='0'))
      assists.append(response.css(search_assists).get(default='0'))

    self.total_years.append(year)
    self.total_names[year] = names
    self.total_points[year] = points
    self.total_rebounds[year] = rebounds
    self.total_assists[year] = assists

    self.save(year)


  def save(self, year):

    filename = "data/data_" + str(year) + ".csv"

    with io.open(filename, 'w', encoding="utf-8", newline='') as csvfile:
      writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
      writer.writerow(["Name", "PPG", "RPG", "APG"])
      for player_name, player_points, player_rebounds, player_assists in zip(self.total_names[year], self.total_points[year], self.total_rebounds[year], self.total_assists[year]):
        if (str(player_name)).strip() != "None":
          writer.writerow([str(player_name), float(player_points), float(player_rebounds), player_assists])