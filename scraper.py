import requests
import csv
import time

def scrape_anime(ids):
    base_url = "https://api.myanimelist.net/v2/anime"
    fields = "mean,num_list_users,genres,start_date"
    output = "mal_anime_data.csv"
    
    with open("auth", "r") as file:
        auth = file.read().strip()
    
    headers = {"X-MAL-CLIENT-ID": auth}
    timeout = 10

    with open(output, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        
        writer.writerow(["ID", "TITLE", "SCORE", "MEMBERS", "GENRES", "START_DATE"])

        for i in range(1, ids):
            url = f"{base_url}/{i}?fields={fields}"
            attempts = 0
            sleep_time = 2
            
            while attempts < 10:
                try:
                    response = requests.get(url, headers=headers, timeout=timeout)
                    if response.status_code == 200:
                        data = response.json()
                        
                        writer.writerow([
                            data.get("id", ""),
                            data.get("title", ""),
                            data.get("mean", ""),
                            data.get("num_list_users", ""),
                            data.get("genres", ""),
                            data.get("start_date", "")
                        ])
                        
                        print(f"✅ Saved: {data['title']} (ID: {i})")
                        break
                    
                    elif response.status_code == 404:
                        print(f"❌ ID {i} not found, skipping.")
                        break

                    elif response.status_code == 429 or 500 <= response.status_code <= 600:
                        print(f"🔥 Rate limited or server error! Sleeping for {sleep_time} seconds...")
                        time.sleep(sleep_time)
                        sleep_time *= 2
                        attempts += 1
                        continue
                    else:
                        print(f"Unexpected error {response.status_code}: {response.text}")
                        break
                
                except requests.exceptions.Timeout:
                    print(f"⏳ Timeout! MAL took too long for ID {i}, sleeping {sleep_time}s and retrying...")
                    time.sleep(sleep_time)
                    sleep_time *= 2
                    attempts += 1

                except Exception as e:
                    print(f"🚨 Error with ID {i}: {e}")
                    time.sleep(sleep_time)
                    sleep_time *= 2
                    attempts += 1

            time.sleep(0.5)

    print(f"\nSaved data to {output}")

def scrape_manga(ids):
    pass