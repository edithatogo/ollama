# LFM2-ColBERT Ollama Modelfile

Use this Modelfile after converting the Hugging Face checkpoint to GGUF.

```modelfile
FROM ./LFM2-ColBERT-350M.gguf

PARAMETER num_ctx 32768
```

Validation:

```sh
ollama create lfm2-colbert-350m -f Modelfile
ollama embed lfm2-colbert-350m "Mars is the Red Planet."
curl -s http://127.0.0.1:11434/api/embed \
  -H 'Content-Type: application/json' \
  -d '{"model":"lfm2-colbert-350m","input":["Mars is the Red Planet.","Jupiter is the largest planet."]}'
```

Expected behavior:

- The model is detected as an embedding model from GGUF `lfm2.pooling_type`.
- The returned vector length is the ColBERT dense projection size, typically 128.
- The `/api/embed` response contains one normalized vector per input string.
