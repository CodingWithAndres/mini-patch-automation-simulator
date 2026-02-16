FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# default command runs the automation then prints report
CMD ["bash", "-lc", "python patcher.py && python report.py"]
