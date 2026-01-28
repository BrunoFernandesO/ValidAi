import { useState } from "react";
import { validateImage } from "../services/validationService.js";
import ResultsList from "./ResultsList";
import Upload from "./Upload.jsx";
import LoadingBar from "./LoadingBar.jsx";

export default function Container() {
  const [results, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);

  const handleSubmit = async (files) => {
  console.log("handleSubmit files:", files);
  console.log("isArray:", Array.isArray(files));
  console.log("length:", files?.length);

    if (loading) return;

    setLoading(true);
    setResult(null);

    try {
      const data = await validateImage(files, setProgress, setLoading);
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


      {results && <ResultsList results={results} />}
    </div>
  );
}
