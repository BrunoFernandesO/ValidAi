import { useDropzone } from "react-dropzone";

export default function Upload({ onUpload, loading }) {

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    multiple: true,
    
    onDrop: async (acceptedFiles) => {
      if (acceptedFiles.length > 0) {
        await onUpload(acceptedFiles);
      }
    },
  });

  return (
    <div
      {...getRootProps()}
      className={`flex flex-col justify-center items-center bg-black/20 outline outline-gray-700/50 backdrop-blur-sm text-gray-400 text-lg xl:text-lg px-8 py-20 rounded-lg border-2 border-dashed border-gray-600 cursor-pointer hover:border-gray-500 hover:bg-black/15 transition-colors text-center ${isDragActive ? "bg-black/25 border-gray-500" : ""}`}
    >
      <input {...getInputProps()} />

      {loading ? (
        <>
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            strokeWidth={1.5}
            stroke="currentColor"
            className="size-20 mb-4 animate-spin"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0 3.181 3.183a8.25 8.25 0 0 0 13.803-3.7M4.031 9.865a8.25 8.25 0 0 1 13.803-3.7l3.181 3.182m0-4.991v4.99"
            />
          </svg>

          <p>Validando imagem...</p>
        </>
      ) : isDragActive ? (
        <>
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            strokeWidth={1.5}
            stroke="currentColor"
            className="size-20 mb-4"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M12 16.5V9.75m0 0 3 3m-3-3-3 3M6.75 19.5a4.5 4.5 0 0 1-1.41-8.775 5.25 5.25 0 0 1 10.233-2.33 3 3 0 0 1 3.758 3.848A3.752 3.752 0 0 1 18 19.5H6.75Z"
            />
          </svg>
          <p>Solte a imagem aqui...</p>
        </>
      ) : (
        <>
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            strokeWidth={1.5}
            stroke="currentColor"
            className="size-20 mb-4"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M12 16.5V9.75m0 0 3 3m-3-3-3 3M6.75 19.5a4.5 4.5 0 0 1-1.41-8.775 5.25 5.25 0 0 1 10.233-2.33 3 3 0 0 1 3.758 3.848A3.752 3.752 0 0 1 18 19.5H6.75Z"
            />
          </svg>
          <p>Arraste a imagem ou clique para selecionar</p>
        </>
      )}
    </div>
  );
}
