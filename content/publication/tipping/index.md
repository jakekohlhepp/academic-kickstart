+++
title = "Is Tipping Incentive Relevant?"

# Date first published.
date = "2025-09-07"

# Authors. Comma separated list, e.g. `["Bob Smith", "David Jones"]`.
authors = ["Jacob Kohlhepp"]

# Publication type.
# Legend:
# 0 = Uncategorized
# 1 = Conference proceedings
# 2 = Journal
# 3 = Work in progress
# 4 = Technical report
# 5 = Book
# 6 = Book chapter
publication_types = ["4"]

# Publication name and optional abbreviated version.
publication = "NEW"
publication_short = ""

# Abstract and optional shortened version.
abstract = ""
# Featured image thumbnail (optional)
#image_preview = ""

# Is this a selected publication? (true/false)
selected = true

# Projects (optional).
#   Associate this publication with one or more of your projects.
#   Simply enter the filename (excluding '.md') of your project file in `content/project/`.
#   E.g. `projects = ["deep-learning"]` references `content/project/deep-learning.md`.
projects = []

# Links (optional).

url_pdf = "pdf/tipping_paper.pdf"
url_preprint = ""
url_code = ""
url_dataset = ""
url_project = ""
url_slides = "" 
#pdf/tipping_slides.pdf
url_video = ""
url_poster = ""
url_source = ""

# Custom links (optional).
#   Uncomment line below to enable. For multiple links, use the form `[{...}, {...}, {...}]`.
# url_custom = [{name = "Custom Link", url = "http://example.org"}]

# Does the content use math formatting?
math = true

# Does the content use source code highlighting?
highlight = true

# Featured image
# Place your image in the `static/img/` folder and reference its filename below, e.g. `image = "example.jpg"`.
[header]
image = "headers/bubbles-wide.jpg"
caption = "My caption 😄"

+++
Whether tips should be treated differently than wages under tax and minimum-wage laws depends on whether they incentivize service quality. I develop a test for incentive relevant tipping, capable of detecting both quality-based social norms and forward-looking behavior, that consists of a simple regression of first-time tip percentages on an indicator for whether a customer returns in the future. I implement the test using more than 200,000 first-time tips from the beauty industry, a setting where the test is high-powered because the customer return rate is 30.7%. Across 2,953 workers, I fail to reject incentive-irrelevant tipping in 98.5% of cases