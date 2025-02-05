from api_token import access_token
import requests
import time
import wget


base_url = "https://api.freeconvert.com/v1"
upload_file_path = "test.pdf"

freeconvert = requests.Session()
freeconvert.headers.update({
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Authorization": f"Bearer {access_token}",
})


def wait_for_job_by_polling(job_id):
  for _ in range(10):
    time.sleep(2)
    job_get_response = freeconvert.get(f"{base_url}/process/jobs/{job_id}")
    job = job_get_response.json()

    if job["status"] == "completed":
      export_task = next(task for task in job["tasks"] if task["name"] == "myExport1")
      wget.download(export_task["result"]["url"])
      print('Download successful')
      return
    elif job["status"] == "failed":
      raise Exception("Job failed")

  raise Exception("Poll timeout")

def upload():
  print("upload example 1")

  upload_task_response = freeconvert.post(f"{base_url}/process/import/upload")
  upload_task_id = upload_task_response.json()["id"]
  uploader_form = upload_task_response.json()["result"]["form"]
  print("Created task", upload_task_id)

  formdata = {}
  for parameter, value in uploader_form["parameters"].items():
    formdata[parameter] = value
  files = {'file': open(upload_file_path, 'rb')}

  # Submit the upload as multipart/form-data request.
  upload_response = requests.post(uploader_form["url"], files=files, data=formdata)
  upload_response.raise_for_status()

  # Use the uploaded file in a job.
  # Job will complete when all its children and dependent tasks are complete.
  job_response = freeconvert.post(f"{base_url}/process/jobs", json={
    "tasks": {
      "myConvert1": {
        "operation": "convert",
        "input": upload_task_id,
        "output_format": "odt",
      },
      "myExport1": {
        "operation": "export/url",
        "input": "myConvert1",
        "filename": "my-converted-file.odt",
      },
    },
  })
  job = job_response.json()
  print("Job created", job["id"])


  wait_for_job_by_polling(job["id"])
