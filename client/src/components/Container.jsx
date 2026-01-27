import { useState } from "react";
import { validateImage } from "../services/validationService.js";
import ResultsList from "./ResultsList";
import Upload from "./Upload.jsx";
import LoadingBar from "./LoadingBar.jsx";

export default function Container() {
  const [results, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);

  const handleSubmit = async (file) => {
    setLoading(true);
    setResult(null);

    try {
      const data = await validateImage(file, setProgress, setLoading);
      setResult(data);
    } catch (error) {
      console.error("handleSubmit error: ", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-gray-800/40 p-5 rounded-lg outline outline-gray-700/50 backdrop-blur-sm text-white gap-8 flex flex-col">
      <Upload
        onUpload={handleSubmit}
        loading={loading}
      />

      <LoadingBar value={progress} />
      <p className="text-sm text-gray-500 mt-1">{progress}%</p>

      {results && <ResultsList results={results} />}
    </div>
  );
}
