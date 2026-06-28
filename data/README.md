# Datasets

Coloca aquí los datasets que consumen los algoritmos del backend.

- `tiktok_combined.txt`: edgelist del grafo de seguidores de TikTok que usa el
  endpoint `GET /api/v1/graph/followers`. Cada línea es una arista dirigida
  `origen destino` (un usuario sigue a otro), por ejemplo:

  ```
  1 2
  1 3
  4 2
  ```

  La ruta se configura con `FOLLOWERS_DATASET_PATH` (ver `.env.example`).

> Los archivos `.txt` de esta carpeta no se versionan (ver `.gitignore`) para no
> subir datasets grandes al repo. Súbelos a tu copia local o ajusta `.gitignore`
> si quieren versionarlos.
