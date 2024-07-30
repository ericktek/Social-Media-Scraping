from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Set up Chrome options
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications": 2}
chrome_options.add_experimental_option("prefs", prefs)

# Specify the path to the ChromeDriver executable
PATH = "/usr/bin/chromedriver"  # Make sure the path is correct
service = Service(PATH)

# Initialize the Chrome WebDriver with the options
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open Facebook
driver.get("https://www.facebook.com")

# Log in to Facebook
username = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "email"))
)
password = driver.find_element(By.ID, "pass")
login_button = driver.find_element(By.NAME, "login")

username.send_keys("masanja") # Replace with your actual username
password.send_keys("*******")  # Replace with your actual password
login_button.click()

# Wait until logged in and the main page is loaded
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='feed']"))
)

# Navigate to the specific post
post_url = "https://www.facebook.com/photo/?fbid=851799316987548&set=a.643562484477900"
driver.get(post_url)

# Wait until the post is loaded
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//div[@class='_6cuy']"))
)

# Load more comments if available
while True:
    try:
        load_more_comments = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[text()='View more comments']"))
        )
        load_more_comments.click()
        time.sleep(2)  # Wait for comments to load
    except:
        break

# Collect comments
comments = driver.find_elements(By.XPATH, "//div[@class='_6cuy']")
for comment in comments:
    print(comment.text)

# Collect number of likes
try:
    likes_element = driver.find_element(By.XPATH, "//div[@class='_3dlh _3dli']/span")
    likes = likes_element.text
    print(f"Likes: {likes}")
except:
    print("Likes information not found.")

# Close the browser
driver.quit()
