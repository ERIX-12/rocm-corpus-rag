FROM rocm/pytorch:rocm10.0_ubuntu26.04_py3.14_pytorch_release_2.13.0
WORKDIR /app
ENV PYTHONUNBUFFERED=1
RUN pip install --no-cache-dir pypdf python-docx openpyxl pillow && \
    pip install --no-cache-dir --no-deps -U transformers tokenizers safetensors && \
    python3 -c "import torch; print(torch.__version__)" && \
    mkdir -p /app/output /app/corpus /models
COPY . /app
RUN chmod +x /app/app.py
CMD ["tail", "-f", "/dev/null"]
