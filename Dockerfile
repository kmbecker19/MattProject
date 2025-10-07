FROM python:3.9

ADD . . 
ADD filter_json.py .
ADD watch_dir.py .

RUN pip install jsonpath-ng watchdog pytest

CMD ["python", "watch_dir.py"]