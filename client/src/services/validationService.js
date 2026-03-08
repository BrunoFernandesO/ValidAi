import axios from "axios";

export async function uploadImage(files, setProgress, filters) {
  const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL,
  });

  const formData = new FormData();
  for (const file of Array.from(files)) {
    formData.append("files", file);
  }

  if (filters.max_size != null) {
    formData.append("max_size", filters.max_size);
  }
  if (filters.expected_width != null) {
    formData.append("expected_width", filters.expected_width);
  }
  if (filters.expected_height != null) {
    formData.append("expected_height", filters.expected_height);
  }
  if (filters.expected_extensions != null) {
    formData.append("expected_extensions", filters.expected_extensions);
  }

  const response = await api.post("/validate", formData, {
    onUploadProgress: (event) => {
      if (!event.total) {
        return;
      }

      const totalPercent = (event.loaded / event.total) * 100;
      setProgress(Math.round(totalPercent));
    },
  });

  setProgress(100);

  return {
    results: response.data.results ?? [],
    batchDownloadUrl: response.data.batch_download_url ?? null,
  };
}
