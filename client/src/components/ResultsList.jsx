import React from "react";

export default function ResultsList({ results }) {
  if (!results || results.length === 0) {
    return <p>Nenhum resultado disponível.</p>;
  }

  const { checks } = results;

  return (
    <div className="overflow-x-auto">
      {results.summary}
      <table className="w-full h-full text-sm text-left border-collapse overflow-hidden text-gray-500 dark-text-gray-400">
        <thead className="text-sm text-black uppercase dark:text-gray-300 bg-gray-50 dark:bg-gray-600/65 h-12">
          <tr>
            <th scope="col" className="px-6 py-3 rounded-l-md">
              Status
            </th>
            <th scope="col" className="px-6 py-3">
              Nome do Arquivo
            </th>
            <th scope="col" className="px-6 py-3">
              Tamanho
            </th>
            <th scope="col" className="px-6 py-3">
              Erro no Tamanho
            </th>
            <th scope="col" className="px-6 py-3">
              Resolução
            </th>
            <th scope="col" className="px-6 py-3 rounded-r-md">
              Erro na Resolução
            </th>
          </tr>
        </thead>
        <tbody>
          <tr className="border-b dark:border-gray-700 border-gray-200">
            <td scope="row" className="px-6 h-18">
              <p className="text-white text-base font-medium text-[0.95rem]">
                {results.approved ? (
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
                    stroke-width="1.5"
                    stroke="#ff0000"
                    class="size-6"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      d="M6 18 18 6M6 6l12 12"
                    />
                  </svg>
                )}
              </p>
            </td>
            <td className="flex h-full items-center gap-2 px-6 py-3">
              <img
                src="https://cdn.pixabay.com/photo/2023/02/18/11/00/icon-7797704_640.png"
                alt=""
                className="w-8 rounded-sm"
              />
              <p className="text-gray-400 font-medium text-[0.8rem] ">{name}</p>
            </td>

            {Array.isArray(checks) &&
              checks.map((check, index) => (
                <React.Fragment key={index}>
                  <td className="px-6 py-3 font-normal text-base text-gray-900 dark:text-gray-200">
                    {check.value}
                  </td>

                  <td>
                    {check.errors?.length > 0 ? (
                      check.errors.map((error, idx) => (
                        <div
                          key={idx}
                          className="px-6 py-3 font-normal text-base text-gray-200 "
                        >
                          {error.message}
                        </div>
                      ))
                    ) : (
                      <span className="px-6 py-3 font-normal text-base text-gray-200">
                        Nenhum erro encontrado.
                      </span>
                    )}
                  </td>
                </React.Fragment>
              ))}
          </tr>
        </tbody>
      </table>
    </div>
  );
}
