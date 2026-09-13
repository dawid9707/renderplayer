# app.py
import json
import os
import subprocess
import tempfile
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://fluffy-fortnight-x5p4xq69pj973v76q-3001.app.github.dev",
        "http://localhost:3001",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/transcode")
async def transcode(
    file: UploadFile = File(...),
    settings: str = Form(...),
    args: str = Form(...),
):
    parsed_settings = json.loads(settings)
    ffmpeg_args = json.loads(args)

    with tempfile.TemporaryDirectory() as directory:
        input_path = os.path.join(directory, "input.webm")
        output_ext = parsed_settings["container"]
        output_path = os.path.join(directory, f"output.{output_ext}")

        with open(input_path, "wb") as target:
            target.write(await file.read())

        # Nie uruchamiaj dowolnych komend shellowych.
        # Argumenty powinny pochodzić wyłącznie z walidowanego buildera.
        safe_args = [
            argument.replace("input.webm", input_path)
                    .replace("output." + output_ext, output_path)
            for argument in ffmpeg_args
        ]

        result = subprocess.run(
            ["ffmpeg", "-y", *safe_args],
            capture_output=True,
            text=True,
            timeout=3600,
        )

        if result.returncode != 0:
            return {
                "error": "FFmpeg failed",
                "details": result.stderr[-4000:],
            }

        media_type = {
            "mp4": "video/mp4",
            "webm": "video/webm",
            "mkv": "video/x-matroska",
            "gif": "image/gif",
        }.get(output_ext, "application/octet-stream")

        return FileResponse(
            output_path,
            media_type=media_type,
            filename=f"output.{output_ext}",
        )