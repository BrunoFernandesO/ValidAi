import React from "react";

function buildApiUrl(path) {
  if (!path) {
    return null;
  }

  return `${import.meta.env.VITE_API_URL}${path}`;
}

function resolvePreviewSrc(item) {
  if (!item.file_url) {
    return null;
  }

  return buildApiUrl(item.file_url);
}

function findCheck(item, checkName) {
  return item.checks?.find((check) => check.name === checkName);
}

export default function ResultsList({ results, summary, batchDownloadUrl }) {
  const batchDownloadHref = buildApiUrl(batchDownloadUrl);
  return (
    <div className="overflow-x-auto">
      {summary.total > 0 ? (
        <div className="p-5 flex justify-between w-full text-gray-100 font-medium items-center">
          <p>
            <span className="text-xl">Σ </span> Total: {summary.total}
          </p>
          <p className="text-[#66ff00] flex">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill=""
              viewBox="0 0 24 24"
              strokeWidth={1.5}
              stroke="#66ff00"
              className="size-6"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="m4.5 12.75 6 6 9-13.5"
              />
            </svg>
            Aprovados: {summary.approved}
          </p>
          <p className="text-[#ff0000] flex">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              strokeWidth={1.5}
              stroke="#ff0000"
              className="size-6"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M6 18 18 6M6 6l12 12"
              />
            </svg>
            Rejeitados: {summary.failed}
          </p>
          {batchDownloadHref ? (
            <a
              href={batchDownloadHref}
              download
              className="bg-sky-600 hover:bg-sky-500 text-white text-xs px-3 py-2 rounded-md"
            >
              Download all adjusted images (.zip)
            </a>
          ) : null}
        </div>
      ) : null}

      <table
        className={`w-full h-full text-sm text-left border-collapse overflow-hidden text-gray-500 dark:text-gray-400 ${summary.total > 0 ? "" : "hidden"}`}
      >
        <thead className="text-sm text-black uppercase dark:text-gray-300 bg-gray-50 dark:bg-gray-600/65 h-12">
          <tr>
            <th scope="col" className="px-6 py-3 rounded-l-md">
              Status
            </th>
            <th scope="col" className="px-6 py-3">
              Nome do Arquivo
            </th>
            <th scope="col" className="px-6 py-3">
              Informações
            </th>
            <th scope="col" className="px-6 py-3 rounded-r-md">
              Motivos
            </th>
          </tr>
        </thead>

        <tbody className="font-normal text-base text-gray-300">
          {results.map((item, index) => {
            const autoFitCheck = findCheck(item, "Ajuste automático");
            const dimensionsCheck = findCheck(item, "Dimensões");
            const previewSrc = buildApiUrl(item.file_url);
            const downloadHref = buildApiUrl(item.download_url ?? item.file_url);

            return (
              <tr
                key={`${item.filename}-${index}`}
                className="border-b-2 dark:border-gray-600/65"
              >
                <td scope="row" className="px-6 h-18">
                  {item.approved ? (
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      fill=""
                      viewBox="0 0 24 24"
                      strokeWidth={1.5}
                      stroke="#66ff00"
                      className="size-6"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        d="m4.5 12.75 6 6 9-13.5"
                      />
                    </svg>
                  ) : (
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      fill="none"
                      viewBox="0 0 24 24"
                      strokeWidth={1.5}
                      stroke="#ff0000"
                      className="size-6"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        d="M6 18 18 6M6 6l12 12"
                      />
                    </svg>
                  )}
                </td>

                <td className="h-full gap-2 px-6 py-3">
                  <div className="flex items-center">
                    {previewSrc ? (
                      <img src={previewSrc} className="w-10 rounded-xs mr-3" />
                    ) : null}
                    <p>{item.filename}</p>
                  </div>

                  {autoFitCheck?.status === "ok" ? (
                    <p className="text-xs mt-2 text-sky-300">Auto-fit com padding branco aplicado.</p>
                  ) : null}
                  {dimensionsCheck ? (
                    <p className="text-xs mt-1 text-gray-400">{dimensionsCheck.value}</p>
                  ) : null}

                  {downloadHref ? (
                    <a
                      href={downloadHref}
                      download
                      className="inline-block mt-2 text-xs bg-white/10 hover:bg-white/20 px-2 py-1 rounded"
                    >
                      Download adjusted image
                    </a>
                  ) : null}
                </td>

                <td className="px-6 py-3">
                  <ul>
                    {item.checks?.map((check, idx) => (
                      <li key={idx}>
                        <span className="text-[0.91em]">{check.name}</span>: {check.value || "N/A"}
                      </li>
                    ))}
                  </ul>
                </td>

                <td className="px-6 py-3 text-[0.91em]">
                  <ul>
                    {item.checks?.flatMap((check, idx) =>
                      check.errors?.map((error, eidx) => (
                        <li key={`${idx}-${eidx}`}>{error.message}</li>
                      )) || []
                    )}
                  </ul>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
