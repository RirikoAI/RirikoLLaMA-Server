### Cuda
If you want to fully use your GPU for inferencing, install this instead of the normal torch package
```
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### CPU only
For CPU only inference, use the standard torch package
```
pip install torch
```