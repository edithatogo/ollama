# Upstream PR Notes

## Ollama

Title:

```text
feat: support LFM2 ColBERT embedding checkpoints
```

Summary:

- Accept `Lfm2Model` Hugging Face configs in conversion.
- Parse SentenceTransformers `modules.json` for LFM2 checkpoints.
- Emit `lfm2.pooling_type`, `lfm2.normalize_embeddings`, and dense projection metadata.
- Map SentenceTransformers dense head tensors such as `1_Dense.linear.weight` to `dense_2.weight`.
- Register `lfm2_embed` and `lfm2moe_embed` in the Go-native model path.

Validation:

```sh
go test -count=1 ./convert -run 'TestLFM2'
go test -count=1 ./model/models/lfm2
go test -count=1 ./model -run 'TestModelForArch|TestPopulateFields'
go test -count=1 ./convert ./fs/ggml ./fs/gguf
go test -count=1 ./llama
```

## llama.cpp

Title:

```text
feat: apply dense-2 embedding projection for LFM2 ColBERT models
```

Summary:

- Read optional `lfm2.dense_2_feat_in` and `lfm2.dense_2_feat_out` metadata.
- Create optional LFM2 `dense_2.weight` tensor during model loading.
- Allow the embedding graph to apply a dense-2-only projection head.
- Preserve existing two-layer SentenceTransformers dense head behavior when `dense_3` is also present.

Validation:

```sh
go test -count=1 ./llama
cmake --preset CPU
cmake --build --preset CPU -- -l "$(sysctl -n hw.ncpu)"
```
