require 'net/http'
require 'json'

url_tag = 'https://www.instagram.com/explore/tags/'

text = Net::HTTP.get(URI.parse(url_tag + "lifeatshopify/"))

finder_text_start = ('<script type="text/javascript">'
                     'window._sharedData = ')
finder_text_start_len = finder_text_start.length - 1
finder_text_end = ';</script>'

all_data_start = text.index(finder_text_start) + finder_text_start_len + 1
all_data_end = text.index(finder_text_end)
json_str = text[all_data_start, all_data_end - all_data_start]
all_data = JSON.parse(json_str)
img_urls = all_data["entry_data"]["TagPage"][0]["tag"]["media"]["nodes"].map{|pic| pic["display_src"]}
puts(img_urls)
img_sources
