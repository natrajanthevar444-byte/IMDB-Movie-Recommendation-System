# ----------- IMPORTS -----------

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import csv
import time


# ----------- BROWSER SETUP -----------

# Configure Chrome options
options = Options()
options.add_argument("--start-maximized")  # Open browser in maximized mode
options.add_argument("--disable-blink-features=AutomationControlled")  # Reduce bot detection
options.add_argument("user-agent=Mozilla/5.0")  # Set user-agent

# Create Chrome driver
driver = webdriver.Chrome(options=options)

# Create explicit wait (15 seconds max wait time)
wait = WebDriverWait(driver, 15)


# ----------- OPEN IMDb PAGE -----------

url = "https://www.imdb.com/search/title/?title_type=feature&release_date=2024-01-01,2024-12-31"
driver.get(url)

print("Opening IMDb 2024 movies page...")

# Wait until first set of movies loads
wait.until(
    EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, "li.ipc-metadata-list-summary-item")
    )
)

print("Initial movies loaded.")


# ----------- CLICK '50 MORE' UNTIL ALL MOVIES LOAD -----------

while True:
    try:
        # Wait until the "50 more" button becomes clickable
        load_more_button = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(., '50 more')]")
            )
        )

        # Scroll to the button (important for click to work)
        driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            load_more_button
        )

        # Click the button using JavaScript (more reliable)
        driver.execute_script(
            "arguments[0].click();",
            load_more_button
        )

        print("Clicked '50 more' button...")

        # Wait a few seconds for new movies to load
        time.sleep(3)

    except TimeoutException:
        # If button not found, it means all movies are loaded
        print("No more movies to load.")
        break


# ----------- SCRAPE MOVIE DATA -----------

# Get all movie containers
movies = driver.find_elements(
    By.CSS_SELECTOR,
    "li.ipc-metadata-list-summary-item"
)

print("Total movies found:", len(movies))

data = []

# Loop through each movie container
for movie in movies:
    try:
        # Extract movie title
        name = movie.find_element(
            By.CSS_SELECTOR,
            "h3.ipc-title__text"
        ).text

        # Extract short storyline
        storyline = movie.find_element(
            By.CSS_SELECTOR,
            "div.ipc-html-content-inner-div"
        ).text

        # Append data to list
        data.append([name, storyline])

    except:
        # Skip if any movie is missing storyline
        continue


# Close browser
driver.quit()


# ----------- SAVE DATA TO CSV -----------

with open(
    "imdb_2024_movies.csv",
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.writer(file)

    # Write header
    writer.writerow(["Movie Name", "Storyline"])

    # Write movie data
    writer.writerows(data)


print("CSV file created successfully!")
print("Total movies saved:", len(data))