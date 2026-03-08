import { useMemo, useState } from "react";

import Filter from "./Filter.jsx";
import LoadingBar from "./LoadingBar.jsx";
import ResultsList from "./ResultsList";
import Upload from "./Upload.jsx";
import { uploadImage } from "../services/validationService.js";

export default function Container() {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [filters, setFilters] = useState({
    max_size: null,
    expected_width: null,
    expected_height: null,
    expected_extensions: null,
  });

  const summary = useMemo(() => {
    const total = results.length;
    const approved = results.filter((result) => result.approved === true).length;
    const failed = total - approved;

    return { total, approved, failed };
  }, [results]);

  const handleUpload = async (validFiles) => {
    setLoading(true);
    setResults([]);
    setProgress(0);

    try {
      const finalResults = await uploadImage(validFiles, setProgress, filters);
      setResults((previous) => [...previous, ...finalResults]);
    } catch (error) {
      console.error("handleUpload error:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleRejected = (rejectedFiles) => {
    setResults(rejectedFiles);
  };

  const handleFilters = (event) => {
    const { name, value } = event.target;

    setFilters((previous) => ({
      ...previous,
      [name]: value.trim() === "" ? null : value.trim(),
    }));
  };

  return (
    <div className="bg-gray-800/40 p-5 rounded-lg outline outline-gray-700/50 backdrop-blur-sm text-white gap-8 flex flex-col">
      <Filter handleFilters={handleFilters} />

      <Upload
        handleUpload={handleUpload}
        handleRejected={handleRejected}
        loading={loading}
      />

      <LoadingBar value={progress} />

      {results && <ResultsList results={results} summary={summary} />}
    </div>
  );
}
