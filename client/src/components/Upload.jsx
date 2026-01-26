export default function Upload(){
    return (
      <div className="flex flex-col justify-center items-center bg-black/20 outline outline-gray-700/50 backdrop-blur-sm text-gray-400 text-lg xl:text-lg px-8 py-20 rounded-lg border-2 border-dashed border-gray-600 cursor-pointer hover:border-gray-500 hover:bg-gray-800/1 transition-colors text-center">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-10 mb-5">
  <path strokeLinecap="round" strokeLinejoin="round" d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5m-13.5-9L12 3m0 0 4.5 4.5M12 3v13.5" />
</svg>
                  Arraste e solte seus arquivos ou pasta aqui, ou clique para selecionar
      </div>
    )
}