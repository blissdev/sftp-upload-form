from typing import Union

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import HTMLResponse

import paramiko

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def read_root():
    html = """
    <html>
        <head>
            <title>Sample</title>
            <style>
                html, body { height: 100%; }
                body {
                    display: grid;
                    justify-content: center;
                    align-content: center;
                }
            </style>
        </head>
        <body>
            <form method="post" action="/upload" enctype="multipart/form-data">
                <input type="file" name="file" />
                <input type="submit" />
            </form>
        </body>
    </html>
    """
    return html

@app.post("/upload")
def upload_file(
    file: UploadFile = File()
):
    try:
        try:
            tp = paramiko.Transport(("127.0.0.1", 2022))
            tp.connect(username="upload", password="upload")
            sftpClient = paramiko.SFTPClient.from_transport(tp)

            up = sftpClient.putfo(file.file, '/upload.png')

            # Make sure to close all created objects.
            sftpClient.close()

            tp.close()
        except paramiko.ssh_exception.AuthenticationException as err:
            print ("Can't connect due to authentication error [" + str(err) + "]")
        except Exception as err:
            print ("Can't connect due to other error [" + str(err) + "]")

    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()
    return {
        "content_type": file.content_type,
    }

