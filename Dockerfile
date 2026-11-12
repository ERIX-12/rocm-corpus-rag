FROM rocm/pytorch:rocm6.2_ubuntu22.04_py3.10_pytorch_release_2.3.0
WORKDIR /app
ENV PYTHONUNBUFFERED=1
# Use --no-deps on HF libraries so ROCm torch (+rocm) is never overwritten by a CUDA build
RUN pip install --no-cache-dir pypdf python-docx openpyxl pillow && \
    pip install --no-cache-dir --no-deps -U transformers tokenizers safetensors && \
    python3 -c "import torch; print(torch.__version__)" && \
    mkdir -p /app/output /app/corpus
COPY . /app
RUN chmod +x /app/app.py
CMD ["tail", "-f", "/dev/null"]
