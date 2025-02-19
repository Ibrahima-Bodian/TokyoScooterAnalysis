library(httr)
library(lubridate)

start_date <- ymd("2021-01-01")
end_date <- ymd("2021-12-31")
current_date <- start_date

while(current_date <= end_date) {
  date_str <- format(current_date, "%Y-%m-%d")
  url <- sprintf("http://172.22.215.130:8080/data?date=%s&token=YOUR_TOKEN", date_str)
  
  response <- GET(url)
  if(status_code(response) == 200) {
    data <- content(response, "text")
    writeLines(data, paste0("data_", date_str, ".csv"))
  }
  current_date <- current_date + days(1)
}
